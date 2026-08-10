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
        const segmenter = new Intl.Segmenter('en', { granularity: 'grapheme' });

        lines.forEach((lineText, lineIdx) => {
            const rowEl = document.createElement("div");
            rowEl.className = "d-flex flex-nowrap align-items-center w-100 py-1";
            rowEl.style.overflowX = "auto";

            const lineSegments = Array.from(segmenter.segment(lineText)).map(s => s.segment);
            lineSegments.forEach(seg => {
                const span = document.createElement("span");
                span.innerText = seg;
                rowEl.appendChild(span);
                this.spans.push(span);
            });

            // Append Enter symbol block if there is a newline after this line
            if (lineIdx < lines.length - 1) {
                const enterSpan = document.createElement("span");
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
            this.spans[0].className = "active-char";
        }
    }

    onMistake(currentIdx) {
        if (currentIdx < this.spans.length && this.spans[currentIdx]) {
            const span = this.spans[currentIdx];
            span.classList.remove("incorrect-char");
            void span.offsetWidth;
            span.className = "incorrect-char";
            setTimeout(() => {
                if (span && span.classList.contains("incorrect-char")) {
                    span.className = "active-char";
                }
            }, 400);
        }
    }

    onCorrect(newIdx) {
        for (let i = 0; i < this.spans.length; i++) {
            if (i < newIdx) {
                this.spans[i].className = "correct-char";
            } else if (i === newIdx) {
                this.spans[i].className = "active-char";
            } else {
                this.spans[i].className = "";
            }
        }

        // Auto-scroll active block into view smoothly
        if (newIdx < this.spans.length && this.spans[newIdx]) {
            this.spans[newIdx].scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        }
    }

    destroy() {
        this.container.innerHTML = "";
    }
}

window.BlockStyleRenderer = BlockStyleRenderer;
