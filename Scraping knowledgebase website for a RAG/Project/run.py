"""This module contains the main function that orchestrates the execution of scripts to scrape knowledge bases for Fortinet, Palo Alto, NetsKope, and Zscaler."""

import shutil
import Script.RecupKbFortinet
import Script.RecupKbPaloAlto
import Script.RecupKbNETSKOPE
import Script.RecupKbZscaler

def main():
    """Orchestrate the execution of scripts to scrape knowledge bases for Fortinet, Palo Alto, NetsKope, and Zscaler."""
    print('Removing previous knowledge bases . . .')
    
    # Remove previous knowledge base
    shutil.rmtree('KB/KbFortinet')
    shutil.rmtree('KB/KbPaloalto')
    shutil.rmtree('KB/KbNetskope')
    shutil.rmtree('KB/KbZscaler')
    
    print('Knowledge bases removed.')
    
    print("\n")

    print('launching scripts . . .')

    # Launch Fortinet script
    print('Launching Fortinet script...')
    # Display a message to indicate that the script has been launched
    message = """
        ##########################################
        ### Fortinet script has been launched. ###
        ##########################################
        """
    print(message)

    # Execute the Fortinet script
    Script.RecupKbFortinet.main()

    # Display a message to indicate that the knowledge base has been saved
    message = """
        >>> Fortinet knowledge base has been saved. <<<
        """
    print(message)

    print("\n")

    # Launch Palo Alto script
    print('Launching Palo Alto script...')
    # Display a message to indicate that the script has been launched
    message = """
        ###########################################
        ### Palo Alto script has been launched. ###
        ###########################################
        """
    print(message)

    # Execute the Palo Alto script
    Script.RecupKbPaloAlto.main()

    # Display a message to indicate that the knowledge base has been saved
    message = """
        >>> Palo Alto knowledge base has been saved. <<<
        """
    print(message)

    print("\n")

    # Launch NetsKope script
    print('Launching NetsKope script...')
    # Display a message to indicate that the script has been launched
    message = """
        ##########################################
        ### NetsKope script has been launched. ###
        ##########################################
        """
    print(message)

    # Execute the NetsKope script
    Script.RecupKbNETSKOPE.main()

    # Display a message to indicate that the knowledge base has been saved
    message = """
        >>> NetsKope knowledge base has been saved. <<<
        """
    print(message)

    print("\n")

    # Launch Zscaler script
    print('Launching Zscaler script...')
    # Display a message to indicate that the script has been launched
    message = """
        #########################################
        ### Zscaler script has been launched. ###
        #########################################
        """
    print(message)

    # Execute the Zscaler script
    Script.RecupKbZscaler.main()

    # Display a message to indicate that the knowledge base has been saved
    message = """
        >>> Zscaler knowledge base has been saved. <<<
        """
    print(message)

    print("\n")
    print("Process done !")
    
if __name__ == "__main__":
    main()