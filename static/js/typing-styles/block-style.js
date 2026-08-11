/**
 * Block Style Typing Renderer
 * Renders characters in horizontal rounded tile blocks with live color feedback.
 */
class BlockStyleRenderer {
    constructor(containerEl) {
        this.container = containerEl;
        this.spans = [];
    }

    init(screenContent) {
        this.container.innerHTML = "";
        this.container.className = "block-typing-area mb-4 shadow-inner";
        this.spans = [];

        const normalizedContent = screenContent.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
        const lines = normalizedContent.split('\n');

        lines.forEach((lineText, lineIdx) => {
            const rowEl = document.createElement("div");
            rowEl.className = "d-flex flex-nowrap align-items-center w-100 py-1";
            rowEl.style.overflowX = "auto";

            const segmentFn = window.segmentTextIntoGraphemes || function(txt) {
                if (typeof Intl !== 'undefined' && Intl.Segmenter) {
                    return Array.from(new Intl.Segmenter('kn', { granularity: 'grapheme' }).segment(txt)).map(s => s.segment);
                }
                return Array.from(txt);
            };

            const lineSegments = segmentFn(lineText);
            lineSegments.forEach(seg => {
                const span = document.createElement("span");
                span.className = "block-char";
                span.innerText = seg;
                rowEl.appendChild(span);
                this.spans.push(span);
            });

            // Append Enter symbol block if there is a newline after this line
            if (lineIdx < lines.length - 1) {
                const enterSpan = document.createElement("span");
                enterSpan.className = "block-char";
                enterSpan.innerText = '↵';
                enterSpan.title = "Press Enter Key";
                enterSpan.style.color = "#0284c7";
                rowEl.appendChild(enterSpan);
                this.spans.push(enterSpan);
            }

            this.container.appendChild(rowEl);
        });

        // Set initial first block active
        if (this.spans.length > 0) {
            this.spans[0].className = "block-char active-char";
        }
    }

    onKeyTyped(typedChar, expectedChar, idx, isCorrect) {
        if (idx < this.spans.length && this.spans[idx]) {
            const span = this.spans[idx];
            span.classList.remove("active-char");
            if (isCorrect) {
                span.className = "block-char correct-char";
            } else {
                span.className = "block-char incorrect-char";
            }
        }

        const nextIdx = idx + 1;
        if (nextIdx < this.spans.length && this.spans[nextIdx]) {
            this.spans[nextIdx].className = "block-char active-char";
            this.spans[nextIdx].scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        }
    }

    onBackspace(newIdx) {
        if (newIdx < 0 || newIdx >= this.spans.length) return;

        // Reset spans from the end down to newIdx
        for (let i = this.spans.length - 1; i > newIdx; i--) {
            if (this.spans[i]) {
                this.spans[i].className = "block-char";
            }
        }

        // Set target span as active
        if (this.spans[newIdx]) {
            this.spans[newIdx].className = "block-char active-char";
            this.spans[newIdx].scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        }
    }

    onMistake(currentIdx) {
        if (currentIdx < this.spans.length && this.spans[currentIdx]) {
            const span = this.spans[currentIdx];
            span.classList.remove("active-char");
            span.classList.remove("incorrect-char");
            void span.offsetWidth;
            span.className = "block-char incorrect-char";
            setTimeout(() => {
                if (span && span.classList.contains("incorrect-char")) {
                    span.className = "block-char active-char";
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

window.BlockStyleRenderer = BlockStyleRenderer;
