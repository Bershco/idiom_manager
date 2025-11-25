# Sun Valley Dark Theme
package require Tk 8.6

namespace eval ttk::theme::sun-valley-dark {
    variable version 1.0
}

proc load_sunvalley_theme_dark {} {

    ttk::style theme create sun-valley-dark -parent default -settings {

        # Global background / foreground
        ttk::style configure . \
            -background "#1E1E1E" \
            -foreground "#FFFFFF"

        # Frame & Label backgrounds
        ttk::style configure TFrame \
            -background "#1E1E1E"

        ttk::style configure TLabel \
            -background "#1E1E1E" \
            -foreground "#FFFFFF"

        # Entry widget
        ttk::style configure TEntry \
            -padding 6 \
            -borderwidth 1 \
            -relief solid \
            -fieldbackground "#2A2A2A" \
            -foreground "#FFFFFF" \
            -background "#2A2A2A"

        # --- BUTTONS ---
        ttk::style configure TButton \
            -padding {8 4} \
            -relief flat \
            -background "#333333" \
            -foreground "#FFFFFF"

        ttk::style map TButton \
            -background {
                active "#444444"
                pressed "#555555"
                !disabled "#333333"
            } \
            -foreground {
                disabled "#777777"
            }
    }
}

load_sunvalley_theme_dark
