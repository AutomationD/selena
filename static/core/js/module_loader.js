var ModuleLoader = {
    'module_names': [],
    'modules': [],

    'load_modules': function (module_names) {
        this.module_names = module_names;
        this.cur_mod_index = -1;
        this.load_next_module();

    },

    'load_next_module': function() {
        this.cur_mod_index++;
        if ( this.cur_mod_index < this.module_names.length ) {
            this.load_module(this.module_names[this.cur_mod_index]);
        }
        else {
            this.on_all_modules_loaded();
        }
    },

    'cur_mod_index': -1,
    'loaded': false,

    'load_module': function (module_name) {
        this.loaded = false;
        var scr = document.createElement('script');
        scr.src = 'modules/' + module_name + '/js/' + module_name + '.js';

        var loader = this;
        var html_head = document.getElementsByTagName("head")[0];

        scr.onload = scr.onreadystatechange = function() {
            if ( !loader.loaded && (!this.readyState || this.readyState == 'loaded' || this.readyState == 'complete') ) {
                loader.loaded = true;

                var module = getModule();
                loader.modules.push(module);

                this.onload = null;
                this.onreadystatechange = null;
                html_head.removeChild(this);

                loader.load_next_module();
            }
        }

        html_head.appendChild(scr);
    },

    'on_all_modules_loaded': function() {}

};
