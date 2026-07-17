(() => {
  const SELECTOR = ".midnight-mark[data-tooltip]";
  const MARGIN = 12;
  const GAP = 9;
  let tooltip = null;
  let activeMark = null;

  function ensureTooltip(container) {
    if (!tooltip) {
      tooltip = document.createElement("div");
      tooltip.id = "midnightTooltip";
      tooltip.className = "midnight-tooltip";
      tooltip.setAttribute("role", "tooltip");
      tooltip.hidden = true;
    }
    if (tooltip.parentElement !== container) container.appendChild(tooltip);
    return tooltip;
  }

  function positionTooltip() {
    if (!activeMark || !tooltip || tooltip.hidden) return;
    const dialog = activeMark.closest("dialog[open]");
    const bounds = dialog?.getBoundingClientRect() || {
      left: 0,
      top: 0,
      right: window.innerWidth,
      bottom: window.innerHeight,
      width: window.innerWidth,
      height: window.innerHeight,
    };
    tooltip.style.width = `${Math.max(120, Math.min(270, bounds.width - MARGIN * 2))}px`;
    const markRect = activeMark.getBoundingClientRect();
    const tipRect = tooltip.getBoundingClientRect();
    const minLeft = bounds.left + MARGIN;
    const maxLeft = Math.max(minLeft, bounds.right - tipRect.width - MARGIN);
    const centeredLeft = markRect.left + markRect.width / 2 - tipRect.width / 2;
    const left = Math.min(Math.max(centeredLeft, minLeft), maxLeft);
    const above = markRect.top - tipRect.height - GAP;
    const below = markRect.bottom + GAP;
    const minTop = bounds.top + MARGIN;
    const maxTop = Math.max(minTop, bounds.bottom - tipRect.height - MARGIN);
    const top = above >= minTop ? above : Math.min(Math.max(below, minTop), maxTop);

    tooltip.style.left = `${Math.round(left)}px`;
    tooltip.style.top = `${Math.round(top)}px`;
  }

  function showTooltip(mark) {
    const copy = mark?.dataset.tooltip?.trim();
    if (!copy) return;
    if (activeMark && activeMark !== mark) activeMark.removeAttribute("aria-describedby");
    activeMark = mark;
    const tip = ensureTooltip(mark.closest("dialog[open]") || document.body);
    tip.textContent = copy;
    tip.hidden = false;
    mark.setAttribute("aria-describedby", tip.id);
    positionTooltip();
  }

  function hideTooltip(mark = null) {
    if (!activeMark || (mark && mark !== activeMark)) return;
    activeMark.removeAttribute("aria-describedby");
    activeMark = null;
    if (tooltip) tooltip.hidden = true;
  }

  document.addEventListener("pointerover", (event) => {
    const mark = event.target.closest?.(SELECTOR);
    if (mark && !mark.contains(event.relatedTarget)) showTooltip(mark);
  });

  document.addEventListener("pointerout", (event) => {
    const mark = event.target.closest?.(SELECTOR);
    if (mark && !mark.contains(event.relatedTarget)) hideTooltip(mark);
  });

  document.addEventListener("focusin", (event) => {
    const mark = event.target.closest?.(SELECTOR);
    if (mark) showTooltip(mark);
  });

  document.addEventListener("focusout", (event) => {
    const mark = event.target.closest?.(SELECTOR);
    if (mark) hideTooltip(mark);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") hideTooltip();
  });

  window.addEventListener("resize", positionTooltip);
  window.addEventListener("scroll", positionTooltip, true);
})();
