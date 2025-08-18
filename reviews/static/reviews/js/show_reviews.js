document.addEventListener('DOMContentLoaded', ()=> {
    const addBtn = document.getElementById('add-button');
    const overlay = document.getElementById('overlay');
    const subBtn = document.getElementById('submit-btn');
    const backBtn = document.getElementById('back-btn');
    const form = document.getElementById('review-form');

    addBtn.addEventListener('click', () => {
        showElement(overlay);

        document.getElementById('add-review').value = '';
    });

    subBtn.addEventListener('click', () => {
        subBtn.disabled = true;
        subBtn.textContent = 'Loading..'

        form.submit();
    })

    
    backBtn.addEventListener('click', () => {
        hideElement(overlay);
        subBtn.disabled = false;
        subBtn.textContent = 'Submit';
    });

    function showAnalysis(id){
        const showAnalysisBtn = document.getElementById(`show-analysis-btn-${id}`)
        const hideAnalysisBtn = document.getElementById(`hide-analysis-btn-${id}`);
        const showAnalysisDiv = document.getElementById(`show-analysis-${id}`);

        hideElement(showAnalysisBtn);
        showElement(hideAnalysisBtn);

        showElement(showAnalysisDiv);

        hideAnalysisBtn.addEventListener('click', () => {
            hideElement(showAnalysisDiv);
            hideElement(hideAnalysisBtn);

            showElement(showAnalysisBtn);
        })
    }

    function showElement(el){
        el.classList.remove('hidden');
        el.classList.add('flex');
    }

    function hideElement(el){
        el.classList.remove('flex');
        el.classList.add('hidden');
    }

    window.showAnalysis = showAnalysis;
})