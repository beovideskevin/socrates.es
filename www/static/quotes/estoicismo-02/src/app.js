const onxrloaded = () => {
    XR8.XrController.configure({
        imageTargetData: [
            // Rome
            require('../image-targets/seneca_05.json'),
            require('../image-targets/epicteto_01.json'),
            require('../image-targets/marcoaurelio_01.json'),
            require('../image-targets/marcoaurelio_02.json'),
        ],
    });
};

window.XR8 ? onxrloaded() : window.addEventListener('xrloaded', onxrloaded);
