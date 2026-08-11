/**
 * Jump Style Platformer Typing Renderer
 * Renders cute cartoon sky/forest scene with staggered wooden branch platforms,
 * words/chunks on branches, and an animated jumping robot character.
 */
class JumpStyleRenderer {
    constructor(containerEl) {
        this.container = containerEl;
        this.platforms = [];
        this.currentPlatformIdx = 0;
        this.charElements = [];
        this.characterEl = null;
        this.stageEl = null;
        this.soundEnabled = true;
        this.audioCtx = null;
    }

    playJumpSound() {
        if (!this.soundEnabled) return;
        try {
            if (!this.audioCtx) {
                this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (this.audioCtx.state === 'suspended') {
                this.audioCtx.resume();
            }
            const osc = this.audioCtx.createOscillator();
            const gain = this.audioCtx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(320, this.audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(700, this.audioCtx.currentTime + 0.18);
            gain.gain.setValueAtTime(0.15, this.audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, this.audioCtx.currentTime + 0.18);
            osc.connect(gain);
            gain.connect(this.audioCtx.destination);
            osc.start();
            osc.stop(this.audioCtx.currentTime + 0.18);
        } catch (e) {}
    }

    init(screenContent) {
        this.container.innerHTML = "";
        this.container.className = "jump-game-container mb-4 shadow-sm";
        this.platforms = [];
        this.currentPlatformIdx = 0;
        this.charElements = [];

        // 1. Background Clouds
        const cloud1 = document.createElement("div");
        cloud1.className = "jump-cloud jump-cloud-1";
        const cloud2 = document.createElement("div");
        cloud2.className = "jump-cloud jump-cloud-2";
        this.container.appendChild(cloud1);
        this.container.appendChild(cloud2);

        // 2. Tree Leaves on Left & Right
        const leftTree = document.createElement("div");
        leftTree.className = "jump-forest-tree";
        leftTree.innerHTML = `
            <svg viewBox="0 0 120 400" width="100%" height="100%" preserveAspectRatio="none">
                <path d="M-20 0 L90 80 L30 110 L110 190 L40 220 L100 320 L-20 380 Z" fill="#22c55e" opacity="0.85"/>
                <path d="M-20 0 L70 70 L20 100 L90 170 L30 200 L80 290 L-20 350 Z" fill="#15803d"/>
            </svg>
        `;
        this.container.appendChild(leftTree);

        // 3. Sound Toggle Button (Top Right)
        const soundBtn = document.createElement("button");
        soundBtn.type = "button";
        soundBtn.className = "jump-sound-btn";
        soundBtn.title = "Toggle Sound Effects";
        soundBtn.innerHTML = `<i class="fa-solid fa-volume-high"></i>`;
        soundBtn.addEventListener("click", () => {
            this.soundEnabled = !this.soundEnabled;
            if (this.soundEnabled) {
                soundBtn.className = "jump-sound-btn";
                soundBtn.innerHTML = `<i class="fa-solid fa-volume-high"></i>`;
            } else {
                soundBtn.className = "jump-sound-btn sound-muted";
                soundBtn.innerHTML = `<i class="fa-solid fa-volume-xmark"></i>`;
            }
        });
        this.container.appendChild(soundBtn);

        // 4. Stage Area for Platforms and Robot
        this.stageEl = document.createElement("div");
        this.stageEl.className = "jump-stage";
        this.container.appendChild(this.stageEl);

        const normalizedContent = screenContent.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
        const segmentFn = window.segmentTextIntoGraphemes || function(txt) {
            if (typeof Intl !== 'undefined' && Intl.Segmenter) {
                return Array.from(new Intl.Segmenter('kn', { granularity: 'grapheme' }).segment(txt)).map(s => s.segment);
            }
            return Array.from(txt);
        };
        const allGraphemes = segmentFn(normalizedContent);

        const chunks = [];
        let curChunk = [];
        for (let i = 0; i < allGraphemes.length; i++) {
            const char = allGraphemes[i];
            curChunk.push({ char: char, globalIdx: i });
            
            // Break chunk at space, newline, or when reaching 4 characters
            if (char === ' ' || char === '\n' || curChunk.length >= 4 || i === allGraphemes.length - 1) {
                // If next character is just a trailing newline or space and chunk isn't full, group it
                if (i + 1 < allGraphemes.length && (allGraphemes[i + 1] === '\n' || allGraphemes[i + 1] === ' ') && curChunk.length < 5) {
                    // continue to grab next whitespace
                } else {
                    chunks.push(curChunk);
                    curChunk = [];
                }
            }
        }
        if (curChunk.length > 0) chunks.push(curChunk);

        // Generate platforms in a guaranteed non-overlapping zig-zag ladder
        const baseTop = 270;
        const stepY = 160;

        chunks.forEach((chunk, pIdx) => {
            const platEl = document.createElement("div");
            platEl.className = "jump-platform";
            
            // Alternating Left (18%) and Right (56%) columns, spaced 160px apart vertically
            const leftVal = (pIdx % 2 === 0) ? '18%' : '56%';
            const topVal = baseTop - (pIdx * stepY);
            
            platEl.style.left = leftVal;
            platEl.style.top = `${topVal}px`;
            platEl.dataset.top = topVal;
            platEl.dataset.left = leftVal;
            platEl.dataset.pIdx = pIdx;

            // Text on platform (crisp white cards)
            const textBox = document.createElement("div");
            textBox.className = "platform-text-box";
            chunk.forEach(item => {
                const charSpan = document.createElement("span");
                charSpan.className = item.globalIdx === 0 ? "platform-char char-active" : "platform-char";
                charSpan.innerText = item.char === ' ' ? '␣' : (item.char === '\n' ? '↵' : item.char);
                charSpan.dataset.globalIdx = item.globalIdx;
                textBox.appendChild(charSpan);
                this.charElements.push(charSpan);
            });
            platEl.appendChild(textBox);

            // Wood Branch Log
            const branch = document.createElement("div");
            branch.className = "platform-wood-branch";
            platEl.appendChild(branch);

            this.stageEl.appendChild(platEl);
            this.platforms.push({
                element: platEl,
                chunk: chunk,
                startIndex: chunk[0].globalIdx,
                endIndex: chunk[chunk.length - 1].globalIdx,
                top: topVal
            });
        });

        // 6. Create Cute Robot Avatar (Matching Image 2)
        this.characterEl = document.createElement("div");
        this.characterEl.className = "jump-character";
        this.characterEl.innerHTML = `
            <svg viewBox="0 0 100 120" width="100%" height="100%">
                <!-- Flower Pot on Head with Sprout -->
                <rect x="36" y="8" width="28" height="14" rx="3" fill="#ca8a04" stroke="#a16207" stroke-width="2"/>
                <path d="M50 8 Q42 -4 34 2" fill="none" stroke="#22c55e" stroke-width="3" stroke-linecap="round"/>
                <path d="M50 8 Q58 -4 66 2" fill="none" stroke="#16a34a" stroke-width="3" stroke-linecap="round"/>
                
                <!-- Robot Head Screen -->
                <rect x="18" y="20" width="64" height="46" rx="14" fill="#60a5fa" stroke="#2563eb" stroke-width="3"/>
                <rect x="25" y="26" width="50" height="34" rx="8" fill="#ffffff"/>
                <!-- Cheerful Face -->
                <path d="M35 38 Q40 33 45 38" fill="none" stroke="#1e3a8a" stroke-width="3" stroke-linecap="round"/>
                <path d="M55 38 Q60 33 65 38" fill="none" stroke="#1e3a8a" stroke-width="3" stroke-linecap="round"/>
                <circle cx="50" cy="46" r="3" fill="#f43f5e"/>
                
                <!-- Robot Body & Limbs -->
                <rect x="30" y="66" width="40" height="26" rx="8" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2.5"/>
                <!-- Arms -->
                <rect x="16" y="68" width="12" height="18" rx="6" fill="#2563eb"/>
                <rect x="72" y="68" width="12" height="18" rx="6" fill="#2563eb"/>
                <!-- Legs -->
                <rect x="36" y="92" width="10" height="18" rx="5" fill="#1e293b"/>
                <rect x="54" y="92" width="10" height="18" rx="5" fill="#1e293b"/>
            </svg>
        `;
        this.stageEl.appendChild(this.characterEl);

        // Position robot on 1st platform
        this.moveCharacterToPlatform(0, false);
    }

    moveCharacterToPlatform(platformIdx, animate = true) {
        if (!this.platforms[platformIdx]) return;
        const plat = this.platforms[platformIdx];
        const platEl = plat.element;

        // Position robot on the right side of the platform
        const left = platEl.offsetLeft + platEl.offsetWidth + 8;
        const top = platEl.offsetTop - 48;

        this.characterEl.style.left = `${left}px`;
        this.characterEl.style.top = `${top}px`;

        // Pan stage smoothly so active platform is always clearly centered in view (Y ~ 220px)
        const cameraOffset = 220 - plat.top;
        this.stageEl.style.transform = `translateY(${cameraOffset}px)`;

        if (animate) {
            this.characterEl.classList.remove("jump-animating");
            void this.characterEl.offsetWidth; // trigger reflow
            this.characterEl.classList.add("jump-animating");
            this.playJumpSound();
        }
    }

    onKeyTyped(typedChar, expectedChar, idx, isCorrect) {
        if (idx < this.charElements.length && this.charElements[idx]) {
            const span = this.charElements[idx];
            span.classList.remove("char-active");
            if (isCorrect) {
                span.className = "platform-char char-done";
            } else {
                span.className = "platform-char char-error";
            }
        }

        const nextIdx = idx + 1;
        if (nextIdx < this.charElements.length && this.charElements[nextIdx]) {
            this.charElements[nextIdx].className = "platform-char char-active";
        }

        // Determine which platform is currently active
        let targetPlatformIdx = 0;
        for (let p = 0; p < this.platforms.length; p++) {
            if (nextIdx >= this.platforms[p].startIndex && nextIdx <= this.platforms[p].endIndex) {
                targetPlatformIdx = p;
                break;
            }
            if (nextIdx > this.platforms[p].endIndex) {
                targetPlatformIdx = Math.min(this.platforms.length - 1, p + 1);
            }
        }

        if (targetPlatformIdx !== this.currentPlatformIdx) {
            this.currentPlatformIdx = targetPlatformIdx;
            this.moveCharacterToPlatform(this.currentPlatformIdx, true);
        }
    }

    onBackspace(newIdx) {
        if (newIdx < 0) return;

        for (let i = this.charElements.length - 1; i > newIdx; i--) {
            if (this.charElements[i]) {
                this.charElements[i].className = "platform-char";
            }
        }

        if (this.charElements[newIdx]) {
            this.charElements[newIdx].className = "platform-char char-active";
        }

        let targetPlatformIdx = 0;
        for (let p = 0; p < this.platforms.length; p++) {
            if (newIdx >= this.platforms[p].startIndex && newIdx <= this.platforms[p].endIndex) {
                targetPlatformIdx = p;
                break;
            }
        }

        if (targetPlatformIdx !== this.currentPlatformIdx) {
            this.currentPlatformIdx = targetPlatformIdx;
            this.moveCharacterToPlatform(this.currentPlatformIdx, true);
        }
    }

    onMistake(currentIdx) {
        if (currentIdx < this.charElements.length && this.charElements[currentIdx]) {
            const span = this.charElements[currentIdx];
            span.classList.remove("char-active");
            span.classList.remove("char-error");
            void span.offsetWidth;
            span.className = "platform-char char-error";
            setTimeout(() => {
                if (span && span.classList.contains("char-error")) {
                    span.className = "platform-char char-active";
                }
            }, 400);
        }
    }

    onCorrect(newIdx) {
        this.onKeyTyped("", "", newIdx - 1, true);
    }

    destroy() {
        this.container.className = "";
        this.container.innerHTML = "";
    }
}

window.JumpStyleRenderer = JumpStyleRenderer;
