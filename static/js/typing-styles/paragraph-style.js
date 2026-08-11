/**
 * Paragraph Style Typing Renderer
 * Matches authentic TypingClub Paragraph / Flow mechanics:
 * - Natural multi-line paragraph layout with clean horizontal divider guidelines.
 * - Monospaced typography with generous tracking.
 * - Active character indicated with blue text and a crisp blue underline cursor (_).
 * - Correct letters turn green.
 * - Incorrect letters turn red with subtle soft red highlight.
 * - Word wrapping for long paragraphs into structured baseline lines.
 * - Continuous non-blocking typing flow with full Backspace / Delete support.
 */
class ParagraphStyleRenderer {
    constructor(containerEl) {
        this.container = containerEl;
        this.charSpans = [];
        this.lineDivs = [];
        this.activeIdx = 0;
        this.rawSegments = [];
    }

    init(screenContent) {
        this.container.className = "";
        this.container.innerHTML = "";
        this.charSpans = [];
        this.lineDivs = [];
        this.activeIdx = 0;

        // Clean white card container with subtle divider lines & smooth scrolling
        this.flowContainer = document.createElement("div");
        this.flowContainer.className = "paragraph-typing-container mb-4";
        this.container.appendChild(this.flowContainer);

        const normalized = screenContent.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
        const rawLines = normalized.split('\n');
        let globalCharIdx = 0;

        const maxCharsPerLine = 44;

        rawLines.forEach((rawLine, lIdx) => {
            const segmentFn = window.segmentTextIntoGraphemes || function(txt) {
                if (typeof Intl !== 'undefined' && Intl.Segmenter) {
                    return Array.from(new Intl.Segmenter('kn', { granularity: 'grapheme' }).segment(txt)).map(s => s.segment);
                }
                return Array.from(txt);
            };
            const lineSegments = segmentFn(rawLine);

            let currentLineEl = document.createElement("div");
            currentLineEl.className = "paragraph-line";
            this.flowContainer.appendChild(currentLineEl);
            this.lineDivs.push(currentLineEl);

            let currentLineCount = 0;

            for (let i = 0; i < lineSegments.length; i++) {
                const char = lineSegments[i];
                const span = document.createElement("span");
                span.className = (globalCharIdx === 0) ? "paragraph-char char-active" : "paragraph-char";
                span.dataset.idx = globalCharIdx;
                span.dataset.expected = char;

                if (char === ' ') {
                    span.innerHTML = "&nbsp;";
                    span.classList.add("char-space");
                } else {
                    span.innerText = char;
                }

                currentLineEl.appendChild(span);
                this.charSpans.push(span);
                globalCharIdx++;
                currentLineCount++;

                // If line exceeds target width and we are at a space or near word boundary, wrap to next line
                if (currentLineCount >= maxCharsPerLine && char === ' ' && i < lineSegments.length - 1) {
                    currentLineEl = document.createElement("div");
                    currentLineEl.className = "paragraph-line";
                    this.flowContainer.appendChild(currentLineEl);
                    this.lineDivs.push(currentLineEl);
                    currentLineCount = 0;
                }
            }

            // If not last line, append Enter symbol marker
            if (lIdx < rawLines.length - 1) {
                const newlineSpan = document.createElement("span");
                newlineSpan.className = (globalCharIdx === 0) ? "paragraph-char char-newline char-active" : "paragraph-char char-newline";
                newlineSpan.dataset.idx = globalCharIdx;
                newlineSpan.dataset.expected = '\n';
                newlineSpan.innerHTML = '<i class="fa-solid fa-arrow-turn-down fa-rotate-90 ms-1 opacity-50 fs-8"></i>';
                
                currentLineEl.appendChild(newlineSpan);
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
        if (this.charSpans[this.activeIdx]) {
            const span = this.charSpans[this.activeIdx];
            const line = span.closest(".paragraph-line");
            if (line && this.flowContainer) {
                const containerRect = this.flowContainer.getBoundingClientRect();
                const lineRect = line.getBoundingClientRect();
                if (lineRect.bottom > containerRect.bottom - 10 || lineRect.top < containerRect.top + 10) {
                    line.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
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
