/**
 * Paragraph Style Typing Renderer
 * Matches authentic TypingClub Paragraph / Flow mechanics:
 * - Natural multi-line paragraph layout with clean baseline line-height.
 * - Word-level wrapping so words and complex Kannada Ottaksharas never clip or overlap.
 * - Active character indicated with bright blue text and crisp underline cursor (_).
 * - Correct letters turn green.
 * - Incorrect letters turn red with soft red highlight.
 * - Smooth auto-scrolling to keep active line in view.
 * - Continuous typing flow with full Backspace / Delete support.
 */
class ParagraphStyleRenderer {
    constructor(containerEl) {
        this.container = containerEl;
        this.charSpans = [];
        this.activeIdx = 0;
        this.flowContainer = null;
    }

    init(screenContent) {
        this.container.className = "";
        this.container.innerHTML = "";
        this.charSpans = [];
        this.activeIdx = 0;

        this.flowContainer = document.createElement("div");
        this.flowContainer.className = "paragraph-typing-container mb-4";
        this.container.appendChild(this.flowContainer);

        const normalized = screenContent.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
        const rawLines = normalized.split('\n');
        let globalCharIdx = 0;

        const segmentFn = window.segmentTextIntoGraphemes || function(txt) {
            if (typeof Intl !== 'undefined' && Intl.Segmenter) {
                return Array.from(new Intl.Segmenter('kn', { granularity: 'grapheme' }).segment(txt)).map(s => s.segment);
            }
            return Array.from(txt);
        };

        rawLines.forEach((rawLine, lIdx) => {
            const lineEl = document.createElement("div");
            lineEl.className = "paragraph-line";
            this.flowContainer.appendChild(lineEl);

            const rawWords = rawLine.split(' ');

            rawWords.forEach((word, wIdx) => {
                const wordEl = document.createElement("span");
                wordEl.className = "paragraph-word";
                lineEl.appendChild(wordEl);

                const wordGraphemes = segmentFn(word);
                for (let i = 0; i < wordGraphemes.length; i++) {
                    const char = wordGraphemes[i];
                    const span = document.createElement("span");
                    span.className = (globalCharIdx === 0) ? "paragraph-char char-active" : "paragraph-char";
                    span.dataset.idx = globalCharIdx;
                    span.dataset.expected = char;
                    span.innerText = char;

                    wordEl.appendChild(span);
                    this.charSpans.push(span);
                    globalCharIdx++;
                }

                // Add space between words
                if (wIdx < rawWords.length - 1) {
                    const spaceSpan = document.createElement("span");
                    spaceSpan.className = (globalCharIdx === 0) ? "paragraph-char char-space char-active" : "paragraph-char char-space";
                    spaceSpan.dataset.idx = globalCharIdx;
                    spaceSpan.dataset.expected = ' ';
                    spaceSpan.innerHTML = "&nbsp;";

                    lineEl.appendChild(spaceSpan);
                    this.charSpans.push(spaceSpan);
                    globalCharIdx++;
                }
            });

            // If not last line, append Enter symbol marker
            if (lIdx < rawLines.length - 1) {
                const newlineSpan = document.createElement("span");
                newlineSpan.className = (globalCharIdx === 0) ? "paragraph-char char-newline char-active" : "paragraph-char char-newline";
                newlineSpan.dataset.idx = globalCharIdx;
                newlineSpan.dataset.expected = '\n';
                newlineSpan.innerHTML = '<i class="fa-solid fa-arrow-turn-down fa-rotate-90 ms-1 opacity-50 fs-8"></i>';

                lineEl.appendChild(newlineSpan);
                this.charSpans.push(newlineSpan);
                globalCharIdx++;
            }
        });

        this.scrollToActive();
    }

    onKeyTyped(typedChar, expectedChar, idx, isCorrect) {
        if (idx < this.charSpans.length && this.charSpans[idx]) {
            const span = this.charSpans[idx];
            span.classList.remove("char-active");

            if (isCorrect) {
                span.classList.remove("char-error");
                span.classList.add("char-correct");
            } else {
                span.classList.remove("char-correct");
                span.classList.add("char-error");
            }
        }

        const nextIdx = idx + 1;
        this.activeIdx = nextIdx;

        if (nextIdx < this.charSpans.length && this.charSpans[nextIdx]) {
            const nextSpan = this.charSpans[nextIdx];
            nextSpan.classList.add("char-active");
            this.scrollToActive();
        }
    }

    onBackspace(newIdx) {
        if (newIdx < 0) return;

        // Reset any spans from activeIdx down to newIdx
        for (let i = this.activeIdx; i >= newIdx; i--) {
            if (i < this.charSpans.length && this.charSpans[i]) {
                const span = this.charSpans[i];
                span.classList.remove("char-active");
                if (i >= newIdx) {
                    span.classList.remove("char-correct");
                    span.classList.remove("char-error");
                }
            }
        }

        this.activeIdx = newIdx;
        if (this.charSpans[newIdx]) {
            this.charSpans[newIdx].classList.add("char-active");
            this.scrollToActive();
        }
    }

    scrollToActive() {
        if (this.charSpans[this.activeIdx] && this.flowContainer) {
            const span = this.charSpans[this.activeIdx];
            const line = span.closest(".paragraph-line") || span;
            const containerRect = this.flowContainer.getBoundingClientRect();
            const lineRect = line.getBoundingClientRect();
            const visualTop = lineRect.top - containerRect.top;
            const visualBottom = lineRect.bottom - containerRect.top;
            const containerHeight = this.flowContainer.clientHeight;

            if (visualTop < 5 || visualBottom > containerHeight - 5) {
                const targetScrollTop = this.flowContainer.scrollTop + visualTop - (containerHeight / 2) + (lineRect.height / 2);
                this.flowContainer.scrollTo({
                    top: Math.max(0, targetScrollTop),
                    behavior: 'smooth'
                });
            }
        }
    }

    onMistake(currentIdx) {
        if (currentIdx < this.charSpans.length && this.charSpans[currentIdx]) {
            const span = this.charSpans[currentIdx];
            span.classList.remove("char-active");
            span.classList.remove("char-error");
            void span.offsetWidth;
            span.classList.add("char-error");
            setTimeout(() => {
                if (span && span.classList.contains("char-error")) {
                    span.classList.remove("char-error");
                    span.classList.add("char-active");
                }
            }, 400);
        }
    }

    destroy() {
        this.container.className = "";
        this.container.innerHTML = "";
    }
}

window.ParagraphStyleRenderer = ParagraphStyleRenderer;
