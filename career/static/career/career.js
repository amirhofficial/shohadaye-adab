(() => {
  const root = document.getElementById('career-quiz-app');
  if (!root) return;

  // فیلتر رشته‌های دانشگاهی و مشاغل
  function setupFilter(buttonSelector, cardSelector, countId, buttonDataKey, fieldAttribute) {
    const buttons = [...document.querySelectorAll(buttonSelector)];
    const cards = [...document.querySelectorAll(cardSelector)];
    const count = document.getElementById(countId);
    if (!buttons.length || !cards.length) return;
    const apply = (value) => {
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset[buttonDataKey] === value)));
      let visible = 0;
      cards.forEach(card => {
        const raw = card.getAttribute(fieldAttribute) || '';
        const show = value === 'all' || (fieldAttribute === 'data-fields' ? raw.trim().split(/\s+/).includes(value) : raw === value);
        card.hidden = !show;
        if (show) visible++;
      });
      if (count) count.textContent = `${visible.toLocaleString('fa-IR')} مورد`;
    };
    buttons.forEach(button => button.addEventListener('click', () => apply(button.dataset[buttonDataKey])));
    apply('all');
  }
  setupFilter('[data-career-filter]', '#major-list .career-list-card', 'major-count', 'careerFilter', 'data-field');
  setupFilter('[data-job-filter]', '#job-list .career-list-card', 'job-count', 'jobFilter', 'data-fields');

  let questions = [], fields = [], answers = [], step = 0;
  try { questions = JSON.parse(root.dataset.questions || '[]'); fields = JSON.parse(root.dataset.fields || '[]'); }
  catch { return; }
  if (!questions.length) return;
  answers = Array(questions.length).fill(null);
  const question = document.getElementById('quiz-question');
  const options = document.getElementById('quiz-options');
  const prev = document.getElementById('quiz-prev');
  const next = document.getElementById('quiz-next');
  const result = document.getElementById('quiz-result');
  const progressText = document.getElementById('quiz-progress-text');
  const progressBar = document.getElementById('quiz-progress-bar');
  const labels = [{ text: 'بله، خیلی', score: 2 }, { text: 'تا حدی', score: 1 }, { text: 'نه چندان', score: 0 }];

  function render() {
    const q = questions[step];
    question.textContent = q.text;
    options.replaceChildren();
    labels.forEach(({ text, score }) => {
      const button = document.createElement('button');
      button.type = 'button'; button.textContent = text;
      button.setAttribute('aria-pressed', String(answers[step] === score));
      button.addEventListener('click', () => { answers[step] = score; render(); });
      options.append(button);
    });
    prev.disabled = step === 0;
    next.disabled = answers[step] === null;
    next.textContent = step === questions.length - 1 ? 'نمایش نتیجه' : 'بعدی';
    progressText.textContent = `پرسش ${step + 1} از ${questions.length}`;
    progressBar.style.width = `${((step + 1) / questions.length) * 100}%`;
    result.hidden = true;
  }
  function showResult() {
    const scores = { math: 0, science: 0, humanities: 0 };
    questions.forEach((q, index) => {
      Object.entries(q.weights || {}).forEach(([field, weight]) => {
        scores[field] = (scores[field] || 0) + answers[index] * weight;
      });
    });
    const ranked = Object.entries(scores).sort((a,b) => b[1]-a[1]);
    const max = ranked[0][1];
    const suggested = max > 0 ? ranked.filter(([, score]) => score >= max * 0.75) : [];
    result.hidden = false;
    result.className = 'quiz-result';
    result.replaceChildren();
    const title = document.createElement('h3');
    title.textContent = suggested.length ? 'حوزه‌هایی که پیشنهاد می‌کنیم بیشتر درباره‌شان بخوانی' : 'هنوز مسیر مشخصی شکل نگرفته؛ این کاملاً طبیعی است';
    result.append(title);
    if (suggested.length) {
      suggested.forEach(([id, score]) => {
        const field = fields.find(x => x.id === id);
        if (!field) return;
        const item = document.createElement('div'); item.className = 'quiz-result__item';
        const heading = document.createElement('h4'); heading.textContent = field.title;
        const desc = document.createElement('p'); desc.textContent = field.slogan;
        const meter = document.createElement('p'); meter.textContent = `هم‌خوانی پاسخ‌ها: ${Math.round(score / max * 100).toLocaleString('fa-IR')}٪`;
        const link = document.createElement('a'); link.className = 'btn btn--primary'; link.href = `/career/field/${id}/`; link.textContent = 'بررسی اطلاعات این رشته';
        item.append(heading, desc, meter, link); result.append(item);
      });
    } else {
      const desc = document.createElement('p'); desc.textContent = 'پیشنهاد می‌کنیم هر سه حوزه را مرور کنی و با مشاور مدرسه گفت‌وگو کنی.'; result.append(desc);
    }
    const hint = document.createElement('p'); hint.textContent = 'این نتیجه فقط یک پیشنهاد اولیه برای آشنایی بیشتر است و نمی‌تواند استعداد یا رشته قطعی تو را مشخص کند.';
    result.append(hint);
    question.textContent = 'نتیجه اولیه آزمون'; options.replaceChildren(); prev.disabled = true; next.disabled = false; next.textContent = 'شروع دوباره';
  }
  prev.addEventListener('click', () => { if (step > 0) { step--; render(); } });
  next.addEventListener('click', () => {
    if (step === questions.length - 1 && !result.hidden) { step = 0; answers.fill(null); render(); return; }
    if (answers[step] === null) return;
    if (step < questions.length - 1) { step++; render(); } else showResult();
  });
  render();
})();
