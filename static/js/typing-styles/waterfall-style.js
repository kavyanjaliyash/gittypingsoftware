/**
 * Waterfall Style Typing Renderer
 * Matches authentic TypingClub waterfall mechanics:
 * - 4 Horizontal track rows with bottom row as the active hit row.
 * - Each letter is aligned horizontally with its corresponding virtual keyboard key below it.
 * - Smooth downward waterfall scroll on correct keystroke.
 * - Instant bright red shake feedback on wrong keystrokes.
 */
class WaterfallStyleRenderer {
    constructor(containerEl) {
        this.container = containerEl;
        this.targetSegments = [];
        this.tracksWrapper = null;
        this.columnBeam = null;
        this.visibleRowsCount = 4;
        this.currentIdx = 0;
    }

    getKeyHorizontalPosition(char) {
        if (!char) return 50;

        let lookup = char.toLowerCase();
        if (char === ' ') lookup = 'Space';
        if (char === '\n') lookup = 'Enter';

        // Check Nudi reverse mapping if applicable
        if (window.nudiReverseMap) {
            if (window.nudiReverseMap[char]) {
                lookup = window.nudiReverseMap[char][0].toLowerCase();
            }
        }

        const shiftSymbols = {
            '~':'`', '!':'1', '@':'2', '#':'3', '$':'4', '%':'5', '^':'6', '&':'7', '*':'8', '(':'9', ')':'0', '_':'-', '+':'=',
            '{':'[', '}':']', '|':'\\', ':':';', '"':'\'', '<':',', '>':'.', '?':'/'
        };
        if (shiftSymbols[lookup]) lookup = shiftSymbols[lookup];

        const keyboardEl = document.getElementById("virtual-keyboard");
        if (!keyboardEl) {
            const defaults = {
                'q': 15, 'w': 22, 'e': 29, 'r': 36, 't': 43, 'y': 50, 'u': 57, 'i': 64, 'o': 71, 'p': 78,
                'a': 18, 's': 25, 'd': 32, 'f': 39, 'g': 46, 'h': 53, 'j': 60, 'k': 67, 'l': 74, ';': 81,
                'z': 22, 'x': 29, 'c': 36, 'v': 43, 'b': 50, 'n': 57, 'm': 64, ',': 71, '.': 78, '/': 85,
                'Space': 50, 'Enter': 90
            };
            return defaults[lookup] || 50;
        }

        try {
            const keyEl = keyboardEl.querySelector(`[data-key="${CSS.escape(lookup)}"]`);
            if (keyEl) {
                const kRect = keyEl.getBoundingClientRect();
                const bRect = keyboardEl.getBoundingClientRect();
                if (bRect.width > 0) {
                    const center = (kRect.left + kRect.width / 2) - bRect.left;
                    return (center / bRect.width) * 100;
                }
            }
        } catch (e) {}

        return 50;
    }

    init(screenContent) {
        this.container.innerHTML = "";
        this.container.className = "waterfall-container mb-4 shadow-sm";

        const normalizedContent = screenContent.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
        const segmentFn = window.segmentTextIntoGraphemes || function(txt) {
            if (typeof Intl !== 'undefined' && Intl.Segmenter) {
                return Array.from(new Intl.Segmenter('kn', { granularity: 'grapheme' }).segment(txt)).map(s => s.segment);
            }
            return Array.from(txt);
        };
        this.targetSegments = segmentFn(normalizedContent);
        this.currentIdx = 0;

        // 1. Vertical Column Guide Beam
        this.columnBeam = document.createElement("div");
        this.columnBeam.className = "waterfall-column-beam";
        this.container.appendChild(this.columnBeam);

        // 2. Tracks Wrapper (Holds 4 horizontal track strips)
        this.tracksWrapper = document.createElement("div");
        this.tracksWrapper.className = "waterfall-tracks-wrapper";
        this.container.appendChild(this.tracksWrapper);

        // Render initial 4 rows
        this.renderTracks(0, false);
    }

    renderTracks(activeIdx, animated = false) {
        this.tracksWrapper.innerHTML = "";

        if (animated) {
            this.tracksWrapper.classList.remove("waterfall-slide-down");
            void this.tracksWrapper.offsetWidth; // trigger reflow
            this.tracksWrapper.classList.add("waterfall-slide-down");
        }

        for (let r = 0; r < this.visibleRowsCount; r++) {
            const segIdx = activeIdx + r;
            const trackRow = document.createElement("div");
            trackRow.className = `waterfall-track-row ${r === 0 ? 'active-track' : ''}`;

            if (segIdx < this.targetSegments.length) {
                const char = this.targetSegments[segIdx];
                const displayChar = char === ' ' ? '␣' : (char === '\n' ? '↵' : char);
                const leftPosPct = this.getKeyHorizontalPosition(char);

                const tile = document.createElement("div");
                tile.className = `waterfall-tile ${r === 0 ? 'active-tile' : ''}`;
                tile.innerText = displayChar;
                tile.style.left = `${leftPosPct}%`;

                trackRow.appendChild(tile);
            }

            this.tracksWrapper.appendChild(trackRow);
        }

        // Update column guide beam position
        if (activeIdx < this.targetSegments.length) {
            const activeChar = this.targetSegments[activeIdx];
            const leftPct = this.getKeyHorizontalPosition(activeChar);
            this.columnBeam.style.left = `calc(${leftPct}% - 30px)`;
            this.columnBeam.style.width = `60px`;
            this.columnBeam.style.display = "block";
        } else {
            this.columnBeam.style.display = "none";
        }
    }

    onKeyTyped(typedChar, expectedChar, idx, isCorrect) {
        const nextIdx = idx + 1;
        this.currentIdx = nextIdx;
        if (nextIdx < this.targetSegments.length) {
            this.renderTracks(nextIdx, true);
        } else {
            // Exercise Completed
            this.tracksWrapper.innerHTML = "";
            const finishRow = document.createElement("div");
            finishRow.className = "waterfall-track-row active-track justify-content-center fw-bold text-success fs-5";
            finishRow.innerHTML = `<i class="fa-solid fa-circle-check me-2"></i> Exercise Finished!`;
            this.tracksWrapper.appendChild(finishRow);
            this.columnBeam.style.display = "none";
        }
    }

    onBackspace(newIdx) {
        if (newIdx < 0) return;
        this.currentIdx = newIdx;
        this.renderTracks(newIdx, false);
    }

    onMistake() {
        this.onKeyTyped("", "", this.currentIdx, false);
    }

    onCorrect(newIdx) {
        this.onKeyTyped("", "", newIdx - 1, true);
    }

    destroy() {
        this.container.className = "";
        this.container.innerHTML = "";
    }
}

window.WaterfallStyleRenderer = WaterfallStyleRenderer;
