"""This module provides a class implementing EntityRecognizer for Transformers pipeline."""

from transformers import pipeline
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer import AnalyzerEngine, EntityRecognizer, RecognizerResult

from presidio_analyzer.nlp_engine import NlpArtifacts,NlpEngineProvider


DEFAULT_ANOYNM_ENTITIES = [
    "[CREDIT_CARD]",
    "[CRYPTO]",
    "[DATE_TIME]",
    "[EMAIL_ADDRESS]",
    "[IBAN_CODE]",
    "[IP_ADDRESS]",
    "[NRP]",
    "[LOCATION]",
    "[PERSON]",
    "[PHONE_NUMBER]",
    "[MEDICAL_LICENSE]",
    "[URL]",
    "[NUMBER]",
    "[Organization]",
]

class TransformerRecognizer(EntityRecognizer):
    """
    Class implementing EntityRecognizer for Transformers pipeline.

    Args:
        model_id_or_path (str): The model id or path to the transformers model.
        mapping_labels (dict): A dictionary mapping transformers labels to presidio labels.
        aggregation_strategy (str, optional): The aggregation strategy to use in the transformers pipeline. Defaults to "simple".
        supported_language (str, optional): The language supported by the class. Defaults to "fr".
        ignore_labels (list, optional): A list of labels to ignore in the transformers pipeline. Defaults to ["O", "MISC"].
    """
    
    def __init__(
        self,
        model_id_or_path: str,
        mapping_labels: dict,
        aggregation_strategy: str = "simple",
        supported_language: str = "fr",
        ignore_labels: list = ["O", "MISC"],
    ):
        """
        Initialize the TransformerRecognizer class.

        Args:
            model_id_or_path (str): The model id or path to the transformers model.
            mapping_labels (dict): A dictionary mapping transformers labels to presidio labels.
            aggregation_strategy (str, optional): The aggregation strategy to use in the transformers pipeline. Defaults to "simple".
            supported_language (str, optional): The language supported by the class. Defaults to "fr".
            ignore_labels (list, optional): A list of labels to ignore in the transformers pipeline. Defaults to ["O", "MISC"].
        """
        # Initializes the transformers pipeline for the given model or path
        self.pipeline = pipeline(
            "token-classification",  # The transformers pipeline type
            model=model_id_or_path,  # The transformers model id or path
            aggregation_strategy=aggregation_strategy,  # The aggregation strategy to use
            ignore_labels=ignore_labels,  # The labels to ignore in the pipeline
        )

        # Maps transformers labels to presidio labels
        self.label2presidio = mapping_labels

        # Passes entities from the model into the parent class
        super().__init__(
            supported_entities=list(self.label2presidio.values()),  # The supported entities by the class
            supported_language=supported_language,  # The supported language by the class
        )

    def load(self) -> None:
        """
        No loading is required.

        This method is part of the EntityRecognizer interface and is called
        to load the model or perform any necessary setup. Since the Transformer
        model is loaded during initialization, there is no need to load it again
        in the load method.
        """
        pass

    def analyze(
        self, text: str, entities = None, nlp_artifacts: NlpArtifacts = None
    ):
        """
        Extract entities using Transformers pipeline.

        Args:
            text (str): The text to analyze
            entities (list, optional): The list of entities to extract. Defaults to None.
            nlp_artifacts (NlpArtifacts, optional): The nlp artifacts. Defaults to None.

        Returns:
            list: A list of RecognizerResult objects
        """
        results = []

        # Predict entities using the transformers pipeline
        predicted_entities = self.pipeline(text)

        # Iterate over the predicted entities
        if len(predicted_entities) > 0:
            for e in predicted_entities:
                # Check if the predicted entity is in the list of entities to extract
                if(e['entity_group'] not in self.label2presidio):
                    continue

                # Convert the predicted entity to a presidio entity
                converted_entity = self.label2presidio[e["entity_group"]]

                # Check if the converted entity is in the list of entities to extract or if no entities are specified
                if converted_entity in entities or entities is None:
                    # Create a RecognizerResult object for the extracted entity
                    results.append(
                        RecognizerResult(
                            entity_type=converted_entity, start=e["start"], end=e["end"], score=e["score"]
                        )
                    )

        # Return the list of extracted entities
        return results

def anonymise_with_transformer(new_text_fr):
    """
    Anonymise the given text using transformer pipeline.

    Args:
        new_text_fr (str): The text to anonymise.

    Returns:
        str: The anonymised text.
    """
    # Mapping of transformer labels to presidio entity types
    mapping_labels = {
        "PER": "[PERSON]",
        "LOC": "[LOCATION]",
        "ORG": "[ORGANIZATION]",
        "PHONE_NUMBER": "[PHONE_NUMBER]",
        "EMAIL_ADDRESS": "[EMAIL_ADDRESS]",
        "CREDIT_CARD": "[CREDIT_CARD]",
        "IBAN_CODE": "[IBAN_CODE]",
        "IP_ADDRESS": "[IP_ADDRESS]",
        "URL": "[URL]",
        "DATE_TIME": "[DATE_TIME]",
        "NRP": "[NRP]",
        "MEDICAL_LICENSE": "[MEDICAL_LICENSE]",
        "CRYPTO": "[CRYPTO]",
    }

    # NLP configuration
    configuration = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": 'fr', "model_name": "fr_core_news_lg"}],
    }

    # List of entities to keep
    to_keep = []
    lang = 'fr'

    # Create NLP engine provider and engine
    provider = NlpEngineProvider(nlp_configuration=configuration)
    nlp_engine = provider.create_engine()

    # Create analyzer engine and add transformer recognizer
    analyzer = AnalyzerEngine(
        nlp_engine=nlp_engine,
        supported_languages="fr"
    )
    transformers_recognizer = TransformerRecognizer(
        "Jean-Baptiste/camembert-ner", mapping_labels
    )
    analyzer.registry.add_recognizer(transformers_recognizer)

    # Analyze text and anonymise it
    analyzer_results = analyzer.analyze(
        text=new_text_fr,
        entities=DEFAULT_ANOYNM_ENTITIES,
        allow_list=to_keep,
        language=lang
    )
    engine = AnonymizerEngine()
    result = engine.anonymize(text=new_text_fr, analyzer_results=analyzer_results)

    # Restructure anonymizer results
    anonymization_results = {
        "anonymized": result.text,
        "found": [entity.to_dict() for entity in analyzer_results]
    }

    # Replace entities with anonymised text in the original text
    words = [
        {
            'word': new_text_fr[obj['start']:obj['end']],
            'entity_type': obj['entity_type'],
            'start': obj['start'],
            'end': obj['end']
        }
        for obj in anonymization_results['found']
    ]
    for word in words:
        new_text_fr = new_text_fr.replace(
            new_text_fr[word['start']:word['end']],
            word['entity_type']
        )

    return new_text_fr
