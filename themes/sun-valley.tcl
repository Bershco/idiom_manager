# Sun Valley Light Theme
package require Tk 8.6

namespace eval ttk::theme::sun-valley {
    variable version 1.0
}

proc load_sunvalley_theme {} {

    ttk::style theme create sun-valley -parent default -settings {

        # Global background / foreground
        ttk::style configure . \
            -background "#FFFFFF" \
            -foreground "#000000"

        # Frame & Label backgrounds
        ttk::style configure TFrame \
            -background "#FFFFFF"

        ttk::style configure TLabel \
            -background "#FFFFFF" \
            -foreground "#000000"

        # Entry widget
        ttk::style configure TEntry \
            -padding 6 \
            -borderwidth 1 \
            -relief solid \
            -fieldbackground "#FFFFFF" \
            -foreground "#000000" \
            -background "#FFFFFF"

        # --- BUTTONS ---
        ttk::style configure TButton \
            -padding {8 4} \
            -relief flat \
            -background "#E7E7E7" \
            -foreground "#000000"

        ttk::style map TButton \
            -background {
                active "#D5D5D5"
                pressed "#C8C8C8"
                !disabled "#E7E7E7"
            } \
            -foreground {
                disabled "#888888"
            }
    }
}

load_sunvalley_theme
