const stopVideoOnTargetLost = {
    schema: {
        video: { type: 'string' },
        thumb: { type: 'string' },
    },
    init() {
        const video = document.querySelector(this.data.video);
        const thumb = document.querySelector(this.data.thumb);

        if (!video || !thumb) {
            console.error('Unable to initialize target video loss handling.');
            return;
        }

        this.onTargetLost = () => {
            video.pause();
            video.currentTime = 0;

            const videoTarget = this.el.querySelector(
                'xrextras-target-video-sound',
            );
            if (!videoTarget) {
                console.error('Unable to restore the target video thumbnail.');
                return;
            }

            // videoTarget.setAttribute('material', 'src', thumb);
        };

        this.el.addEventListener('xrextraslost', this.onTargetLost);
    },
    remove() {
        if (this.onTargetLost) {
            this.el.removeEventListener('xrextraslost', this.onTargetLost);
        }
    },
};

if (typeof AFRAME !== 'undefined') {
    AFRAME.registerComponent('target-video-stop-on-lost', stopVideoOnTargetLost);
}

if (typeof module !== 'undefined') {
    module.exports = stopVideoOnTargetLost;
}
