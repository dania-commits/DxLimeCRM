const personas = {
  salesLead: {
    jobs: [
      "Keep a healthy pipeline that the team trusts",
      "Decide quickly where to focus sales energy",
      "Report to leadership without manual spreadsheet work"
    ],
    pains: [
      "Reps chase low value leads because there is no shared prioritisation logic",
      "Pipeline meetings are reactive and focused on explaining numbers",
      "Difficult to see which activities actually drive deals forward"
    ],
    opportunities: [
      "Provide a clear 'Next best lead' view inside Lime Go",
      "Highlight segments and sources that convert best",
      "Give simple dashboards that are easy to discuss in weekly meetings"
    ]
  },
  ae: {
    jobs: [
      "Hit quota without burning out",
      "Spend more time with the right customers",
      "Move deals forward with clarity on next step"
    ],
    pains: [
      "Too many leads feel the same in the list view",
      "Hard to know which deals are realistically winnable this month",
      "Context is scattered between emails, notes and calls"
    ],
    opportunities: [
      "Surface high-intent accounts with a score and explanation",
      "Show a focused daily view of 10–15 high leverage actions",
      "Tie all activities to a simple progress indicator in Lime Go"
    ]
  },
  founder: {
    jobs: [
      "Build a repeatable sales motion, not just heroic wins",
      "Understand which customers are the best fit",
      "Get quick answers without running new reports each time"
    ],
    pains: [
      "Sales knowledge lives in people, not in systems",
      "Unclear whether money is left on the table in existing pipeline",
      "Hard to compare performance between markets or segments"
    ],
    opportunities: [
      "Use Lime Go as the single source of truth for deals and activities",
      "Create simple, comparable views across segments and countries",
      "Experiment with prioritisation rules and see impact over time"
    ]
  }
};

function renderPersona(key) {
  const persona = personas[key];
  const jobsEl = document.getElementById("personaJobs");
  const painsEl = document.getElementById("personaPains");
  const oppEl = document.getElementById("personaOpportunities");

  jobsEl.innerHTML = "";
  painsEl.innerHTML = "";
  oppEl.innerHTML = "";

  persona.jobs.forEach(j => {
    const li = document.createElement("li");
    li.textContent = j;
    jobsEl.appendChild(li);
  });

  persona.pains.forEach(p => {
    const li = document.createElement("li");
    li.textContent = p;
    painsEl.appendChild(li);
  });

  persona.opportunities.forEach(o => {
    const li = document.createElement("li");
    li.textContent = o;
    oppEl.appendChild(li);
  });
}

document.getElementById("personaSelect").addEventListener("change", (e) => {
  renderPersona(e.target.value);
});

// Initial render
renderPersona("salesLead");

// Discovery summariser
function summariseProblem() {
  const raw = document.getElementById("discoveryInput").value.trim();
  const output = document.getElementById("problemOutput");
  if (!raw) {
    output.textContent = "Add a few discovery notes first – what are people telling us?";
    return;
  }

  const lines = raw
    .split(/\r?\n/)
    .map(l => l.trim())
    .filter(l => l && l.startsWith("-"))
    .map(l => l.replace(/^[-•]\s*/, ""));

  let summary;
  if (lines.length === 0) {
    summary = "The notes are not yet structured as pains or needs. A next step would be to rewrite them as clear problem statements from the customer's perspective.";
  } else {
    summary =
      "From the discovery so far, a strong candidate problem for Lime Go to focus on is:

" +
      "Sales teams waste energy on the wrong leads and struggle to understand which opportunities are most likely to convert. This leads to slow, reactive pipeline reviews and missed revenue. Lime Go can help by offering a simple, explainable prioritisation layer on top of existing data, starting with a focused 'who to talk to next' view.";
  }

  output.textContent = summary;
}

// Funnel simulator
let revenueChart;

function recalculateFunnel() {
  const leads = Number(document.getElementById("leadsInput").value) || 0;
  const win = Number(document.getElementById("winRateInput").value) || 0;
  const winImproved = Number(document.getElementById("improvedWinRateInput").value) || 0;
  const dealValue = Number(document.getElementById("dealValueInput").value) || 0;

  const baselineWins = leads * (win / 100);
  const improvedWins = leads * (winImproved / 100);

  const baselineRevenue = baselineWins * dealValue;
  const improvedRevenue = improvedWins * dealValue;
  const extraRevenue = improvedRevenue - baselineRevenue;

  function fmt(n) {
    if (!isFinite(n)) return "–";
    return new Intl.NumberFormat("sv-SE", { style: "currency", currency: "SEK", maximumFractionDigits: 0 }).format(n);
  }

  document.getElementById("baselineRevenue").textContent = fmt(baselineRevenue);
  document.getElementById("improvedRevenue").textContent = fmt(improvedRevenue);
  document.getElementById("extraRevenue").textContent = fmt(extraRevenue);

  const ctx = document.getElementById("revenueChart").getContext("2d");
  if (revenueChart) revenueChart.destroy();
  revenueChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Baseline", "With prioritised leads"],
      datasets: [
        {
          label: "Monthly revenue (SEK)",
          data: [baselineRevenue, improvedRevenue],
          borderRadius: 6
        }
      ]
    },
    options: {
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          ticks: { color: "#9ca3af" },
          grid: { display: false }
        },
        y: {
          ticks: { color: "#9ca3af" },
          grid: { color: "#1f2937" }
        }
      }
    }
  });
}

recalculateFunnel();

// Initiative prioritisation
const initiatives = [
  {
    name: "Lead focus view with simple score",
    userValue: 9,
    businessValue: 8,
    effort: 4
  },
  {
    name: "Playbooks and next-best-action suggestions",
    userValue: 8,
    businessValue: 9,
    effort: 6
  },
  {
    name: "Advanced multi-region reporting suite",
    userValue: 6,
    businessValue: 7,
    effort: 8
  },
  {
    name: "In-app onboarding tour for new users",
    userValue: 7,
    businessValue: 6,
    effort: 3
  }
];

function computeScore(item) {
  return (item.userValue * 0.4 + item.businessValue * 0.4) / (item.effort * 0.2);
}

function renderInitiatives() {
  const body = document.getElementById("initiativeBody");
  body.innerHTML = "";
  initiatives.forEach(item => {
    const tr = document.createElement("tr");
    const score = computeScore(item);
    tr.innerHTML = `
      <td>${item.name}</td>
      <td>${item.userValue}</td>
      <td>${item.businessValue}</td>
      <td>${item.effort}</td>
      <td>${score.toFixed(1)}</td>
    `;
    body.appendChild(tr);
  });
}

function sortInitiatives() {
  initiatives.sort((a, b) => computeScore(b) - computeScore(a));
  renderInitiatives();
}

renderInitiatives();
