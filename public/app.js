"use strict";

const state = {
  meta: null,
  focus: new Set(),
  controlsDisabled: true,
  requestId: 0,
};

const byId = (id) => document.getElementById(id);

function node(tag, options = {}) {
  const element = document.createElement(tag);
  if (options.className) element.className = options.className;
  if (options.text !== undefined) element.textContent = options.text;
  return element;
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    const message = payload?.error?.message || `HTTP ${response.status}`;
    throw new Error(message);
  }
  return payload;
}

function setStatus(ok, label) {
  const status = byId("api-status");
  status.classList.toggle("is-error", !ok);
  status.lastChild.textContent = ` ${label}`;
}

function setControlsDisabled(disabled) {
  state.controlsDisabled = disabled;
  ["scenario", "limit", "reset-focus", "submit-button"].forEach((id) => {
    byId(id).disabled = disabled;
  });
  document.querySelectorAll(".focus-chip").forEach((button) => {
    button.disabled = disabled;
  });
}

function updateScenarioDescription() {
  const id = byId("scenario").value;
  byId("scenario-description").textContent = state.meta.scenarios[id]?.description || "";
}

function renderFocusGrid() {
  const grid = byId("focus-grid");
  grid.replaceChildren();
  Object.entries(state.meta.focus_taxonomy).forEach(([id, label]) => {
    const button = node("button", { className: "focus-chip" });
    button.type = "button";
    button.disabled = state.controlsDisabled;
    button.dataset.focus = id;
    button.setAttribute("aria-pressed", "false");
    const code = node("small", { text: id });
    code.setAttribute("aria-hidden", "true");
    button.append(node("span", { text: label }), code);
    button.addEventListener("click", () => {
      if (state.focus.has(id)) state.focus.delete(id);
      else state.focus.add(id);
      const active = state.focus.has(id);
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    grid.append(button);
  });
}

function renderMeta() {
  const scenarioSelect = byId("scenario");
  scenarioSelect.replaceChildren();
  Object.entries(state.meta.scenarios).forEach(([id, scenario]) => {
    const option = node("option", { text: `${id} — ${scenario.description}` });
    option.value = id;
    scenarioSelect.append(option);
  });
  scenarioSelect.value = "company";
  scenarioSelect.addEventListener("change", updateScenarioDescription);
  updateScenarioDescription();
  renderFocusGrid();

  byId("meta-investors").textContent = `${state.meta.investors.length}レンズ`;
  byId("meta-scenarios").textContent = `${Object.keys(state.meta.scenarios).length}シナリオ`;
  byId("meta-reviewed").textContent = `確認日 ${state.meta.reviewed_at}`;
}

function detailBlock(title, items, open = false) {
  const details = node("details", { className: "lens-details" });
  details.open = open;
  details.append(node("summary", { text: title }));
  const list = node("ul");
  items.forEach((item) => list.append(node("li", { text: item })));
  details.append(list);
  return details;
}

function sourceBlock(sources) {
  const wrap = node("div", { className: "source-list" });
  wrap.append(node("p", { className: "mini-label", text: "哲学資料" }));
  sources.forEach((source) => {
    const link = node("a", { text: `${source.title} ↗` });
    link.href = source.url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    const kind = node("small", {
      text: state.meta.source_kind_labels[source.kind] || source.kind,
    });
    const row = node("div", { className: "source-row" });
    row.append(link, kind);
    wrap.append(row);
  });
  return wrap;
}

function lensCard(lens, index) {
  const card = node("article", { className: "lens-card" });
  card.style.setProperty("--delay", `${index * 55}ms`);

  const number = node("span", { className: "lens-number", text: String(index + 1).padStart(2, "0") });
  const title = node("div");
  title.append(
    node("p", { className: "mini-label", text: lens.school_ja }),
    node("h3", { text: `${lens.name_ja} · ${lens.name}` })
  );
  const header = node("header", { className: "lens-header" });
  header.append(number, title);

  const scopes = node("div", { className: "tag-row" });
  lens.scope.forEach((scope) => scopes.append(node("span", {
    className: "scope-tag",
    text: state.meta.scope_labels[scope] || scope,
  })));
  lens.matched_focus.forEach((focus) => scopes.append(node("span", {
    className: "match-tag",
    text: state.meta.focus_taxonomy[focus] || focus,
  })));

  card.append(
    header,
    scopes,
    node("p", { className: "lens-summary", text: lens.summary }),
    detailBlock("中核原則", lens.principles, true),
    detailBlock("このレンズが問うこと", lens.questions),
    detailBlock("適用限界", lens.limitations),
    sourceBlock(lens.sources)
  );
  return card;
}

function renderSelection(payload, { focusHeading = false } = {}) {
  const selection = payload.data;
  const root = byId("selection-results");
  root.replaceChildren();

  const heading = node("div", { className: "selection-heading" });
  const headingText = node("div");
  const resultHeading = node("h2", { text: `${selection.selected_lenses.length}つのレンズを選択` });
  resultHeading.tabIndex = -1;
  headingText.append(
    node("p", {
      className: "kicker",
      text: `${state.meta.selection_mode_labels[selection.selection_mode] || selection.selection_mode} · ${selection.scenario}`,
    }),
    resultHeading,
    node("p", { text: selection.scenario_description })
  );
  const reviewed = node("span", { className: "reviewed-badge", text: `資料確認日 ${selection.library_reviewed_at}` });
  heading.append(headingText, reviewed);
  root.append(heading);

  if (selection.uncovered_focus_tags.length) {
    root.append(node("div", {
      className: "warning-box",
      text: `上限内で未カバー: ${selection.uncovered_focus_tags_ja.join("、")}`,
    }));
  }

  const cards = node("div", { className: "lens-grid" });
  selection.selected_lenses.forEach((lens, index) => cards.append(lensCard(lens, index)));
  root.append(cards, node("p", { className: "disclaimer", text: payload.disclaimer }));

  byId("result-placeholder").hidden = true;
  byId("error-box").hidden = true;
  root.hidden = false;
  byId("result-status").textContent = `${selection.selected_lenses.length}つの投資家レンズを選択しました。`;
  if (focusHeading) resultHeading.focus({ preventScroll: false });
}

async function submitSelection(event) {
  if (event) event.preventDefault();
  if (!state.meta) return;
  const requestId = ++state.requestId;
  const button = byId("submit-button");
  const panel = byId("results-panel");
  setControlsDisabled(true);
  button.firstElementChild.textContent = "選定中…";
  panel.setAttribute("aria-busy", "true");

  try {
    const payload = await requestJson("/api?view=select", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        scenario: byId("scenario").value,
        focus_tags: [...state.focus],
        lenses: [],
        limit: Number(byId("limit").value),
      }),
    });
    if (requestId !== state.requestId) return;
    renderSelection(payload, { focusHeading: Boolean(event) });
  } catch (error) {
    if (requestId !== state.requestId) return;
    const box = byId("error-box");
    box.textContent = `選定できませんでした: ${error.message}`;
    box.hidden = false;
    byId("selection-results").hidden = true;
  } finally {
    if (requestId === state.requestId) {
      setControlsDisabled(false);
      button.firstElementChild.textContent = "評議会を選ぶ";
      panel.setAttribute("aria-busy", "false");
    }
  }
}

async function init() {
  try {
    state.meta = await requestJson("/api?view=meta");
    renderMeta();
    setStatus(true, "API 接続済み");
    setControlsDisabled(false);
    await submitSelection();
  } catch (error) {
    setStatus(false, "API 接続不可");
    const box = byId("error-box");
    box.textContent = `初期化に失敗しました: ${error.message}`;
    box.hidden = false;
    byId("results-panel").setAttribute("aria-busy", "false");
  }
}

byId("council-form").addEventListener("submit", submitSelection);
byId("reset-focus").addEventListener("click", () => {
  state.focus.clear();
  document.querySelectorAll(".focus-chip").forEach((button) => {
    button.classList.remove("is-active");
    button.setAttribute("aria-pressed", "false");
  });
});

init();
