const onxrloaded = () => {
    XR8.XrController.configure({
        imageTargetData: [
            // Greece
            require('../image-targets/socrates_01.json'),
            require('../image-targets/diogenes_01.json'),
            require('../image-targets/cleantes_01.json'),
            require('../image-targets/zenon_02.json'),
        ],
    });
};

window.XR8 ? onxrloaded() : window.addEventListener('xrloaded', onxrloaded);
