/* ==========================================
   NLP PREPROCESS - MAIN JS (GLOBAL LOGIC)
   ========================================== */

document.addEventListener('DOMContentLoaded', () => {
    // Highlight Active Navbar Link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Initialize Tooltips or Popovers if Bootstrap available
    if (window.bootstrap && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
});

// Toast notification helper
function showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.position = 'fixed';
        container.style.bottom = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    const bgClass = type === 'error' ? 'bg-danger' : (type === 'success' ? 'bg-success' : 'bg-primary');
    toast.className = `toast align-items-center text-white ${bgClass} border-0 show mb-2`;
    toast.role = 'alert';
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body font-weight-bold">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 4000);
}

// Copy to Clipboard Utility
function copyToClipboard(elementId) {
    const el = document.getElementById(elementId);
    if (!el) return;
    const textToCopy = el.innerText || el.textContent;
    if (!textToCopy.strip()) {
        showToast('Nothing to copy!', 'info');
        return;
    }
    navigator.clipboard.writeText(textToCopy).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(err => {
        showToast('Failed to copy text', 'error');
    });
}

// Helper to run individual technique sandbox demo APIs on deep dive pages
async function runTechniqueDemo(endpoint, payload, outputElId, explanationElId = null, diffContainerId = null) {
    const outputEl = document.getElementById(outputElId);
    if (outputEl) outputEl.innerHTML = '<span class="text-muted"><i class="fas fa-spinner fa-spin"></i> Processing...</span>';

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (!response.ok || !data.success) {
            if (outputEl) outputEl.innerHTML = `<span class="text-danger">${data.error || 'Execution failed.'}</span>`;
            return;
        }

        // Render Output
        if (outputEl) {
            if (Array.isArray(data.output)) {
                outputEl.innerHTML = JSON.stringify(data.output, null, 2);
            } else {
                outputEl.innerText = data.processed || data.output;
            }
        }

        // Render Explanation if provided
        if (explanationElId) {
            const expEl = document.getElementById(explanationElId);
            if (expEl && data.explanation) {
                expEl.innerText = data.explanation;
            }
        }

        // Render Diff if container exists
        if (diffContainerId && data.diff) {
            const diffEl = document.getElementById(diffContainerId);
            if (diffEl) {
                diffEl.innerHTML = data.diff.map(item => {
                    if (item.changed) {
                        return `<span class="token-chip changed">${item.original} &rarr; ${item.processed}</span>`;
                    } else {
                        return `<span class="token-chip">${item.original}</span>`;
                    }
                }).join(' ');
            }
        }
    } catch (err) {
        if (outputEl) outputEl.innerHTML = `<span class="text-danger">Network Error: ${err.message}</span>`;
    }
}
