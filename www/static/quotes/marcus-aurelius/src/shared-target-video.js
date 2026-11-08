const targetVideoSoundComponent = {
    schema: {
        video: { type: 'string' },
        thumb: { type: 'string' },
        height: { type: 'number', default: 1.34 },
        width: { type: 'number', default: 1 },
    },
    init() {
        const v = document.querySelector(this.data.video);
        const thumb = document.querySelector(this.data.thumb);
        let tapped = false;

        this.el.addEventListener('click', () => {
            if (!v) {
                return;
            }

            if (tapped) {
                v.pause();
                v.currentTime = 0;
                this.el.setAttribute('material', 'src', thumb);
                tapped = false;
                return;
            }

            this.el.setAttribute('material', 'src', v);
            v.currentTime = 0;
            v.play();
            tapped = true;
        });

        const foundTarget = () => {
            if (tapped && v) {
                v.play();
            }
        };

        const lostTarget = () => {
            if (tapped && v) {
                v.pause();
                v.currentTime = 0;
                this.el.setAttribute('material', 'src', thumb);
                tapped = false;
            }
        };

        this.el.parentNode.addEventListener('xrextrasfound', foundTarget);
        this.el.parentNode.addEventListener('xrextraslost', lostTarget);
    },
};

if (typeof window !== 'undefined') {
    window.targetVideoSoundComponent = targetVideoSoundComponent;
}

if (typeof module !== 'undefined') {
    module.exports = targetVideoSoundComponent;
}
