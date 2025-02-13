package com.example.myprojectv2.utils;

import android.content.res.Resources;
import android.graphics.Color;
import android.os.Build;

/**
 * This class extends the Resources class and provides custom colors for some specific color IDs.
 * For all other color IDs, it calls the super method of the parent class.
 *
 * @author Maxime Bouet, Sebastien Bois, Paul Monsigny.
 */
public class Res extends Resources{
    /**
     * Constructor that takes a Resources object and passes its assets, display metrics, and configuration to the super constructor.
     *
     * @param original The original Resources object
     */
    public Res(Resources original) {
        super(original.getAssets(), original.getDisplayMetrics(), original.getConfiguration());
    }

    /**
     * Returns the color associated with the given resource ID.
     * If the resource ID matches one of the custom color IDs, it returns the corresponding color.
     * Otherwise, it calls the super method of the parent class to get the color.
     *
     * @param id The resource ID of the color to retrieve
     *
     * @return The color associated with the given resource ID
     *
     * @throws NotFoundException if the given ID does not exist
     */
    @Override public int getColor(int id) throws NotFoundException {
        return getColor(id, null);
    }

    /**
     * Returns the color associated with the given resource ID.
     * If the resource ID matches one of the custom color IDs, it returns the corresponding color.
     * Otherwise, it calls the super method of the parent class to get the color.
     *
     * @param id The resource ID of the color to retrieve
     * @param theme The theme from which to retrieve the color, or null to use the default theme
     *
     * @return The color associated with the given resource ID
     *
     * @throws NotFoundException if the given ID does not exist
     */
    @Override public int getColor(int id, Theme theme) throws NotFoundException {
        switch (id) { // DARK GREY
            case 202020:
                return Color.DKGRAY;
            case 30000: // RED
                return Color.RED;
            case 870883: // MAGENTA
                return Color.MAGENTA;
            case 141497: // DARK BLUE
                return Color.rgb(3,35,145);
            case 884909: // BROWN
                return Color.rgb(110,44,0);
            case 178697: // CYAN
                return Color.rgb(13,189,216);
            case 189025: // GREEN
                return Color.GREEN;
            case 178691: // ORANGE
                return Color.rgb(219,118,11);
            case 178692: // YELLOW
                return Color.rgb(218,208,8);
            default:
                return super.getColor(id, theme);
        }
    }
}
