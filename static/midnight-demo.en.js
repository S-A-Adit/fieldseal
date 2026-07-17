const byId = (id) => document.getElementById(id);
const SUPPORTED_LANGUAGES = ["no", "en", "pl", "lt", "lv"];
const pathLanguage = window.location.pathname.split("/").filter(Boolean)[0];
const currentLanguage = SUPPORTED_LANGUAGES.includes(pathLanguage) ? pathLanguage : "en";
const locales = window.fieldSealReportLocales || window.esenseReportLocales || {};
const locale = locales[currentLanguage] || locales.en;
const fallbackLocale = locales.en || locale;

function copy(key) {
  return locale?.copy?.[key] || fallbackLocale?.copy?.[key] || key;
}

function setText(id, value) {
  const element = byId(id);
  if (element) element.textContent = value ?? "-";
}

function applyLanguage() {
  document.documentElement.lang = currentLanguage;
  document.title = copy("page_title");
  document.querySelectorAll("[data-copy]").forEach((element) => {
    element.textContent = copy(element.dataset.copy);
  });
  document.querySelectorAll("[data-tooltip-key]").forEach((element) => {
    const value = copy(element.dataset.tooltipKey);
    element.dataset.tooltip = value;
    element.setAttribute("aria-label", value);
  });
  const selector = byId("reportLanguage");
  if (selector) {
    selector.value = currentLanguage;
    selector.setAttribute("aria-label", copy("language"));
  }
}

function formatDate(value) {
  if (!value) return "-";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return new Intl.DateTimeFormat(locale.intl, {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    timeZoneName: "short",
  }).format(parsed);
}

function formatVerificationTime() {
  return new Intl.DateTimeFormat(locale.intl, {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  }).format(new Date());
}

function compactIdentifier(value, leading = 12, trailing = 8) {
  if (!value || value.length <= leading + trailing + 1) return value || "-";
  return `${value.slice(0, leading)}...${value.slice(-trailing)}`;
}

function renderTests(sourceItems) {
  const body = byId("testRows");
  body.replaceChildren();
  sourceItems.forEach((item, index) => {
    const row = document.createElement("tr");
    const values = [locale.report.tests[index] || item.test, item.result, locale.report.pass || item.status];
    values.forEach((value) => {
      const cell = document.createElement("td");
      cell.textContent = value;
      row.appendChild(cell);
    });
    body.appendChild(row);
  });
}

function renderParties(items) {
  const list = byId("partyFacts");
  list.replaceChildren();
  items.forEach((item) => {
    const entry = document.createElement("div");
    entry.className = "party-fact";
    const label = document.createElement("span");
    const value = document.createElement("strong");
    label.textContent = item.label;
    value.textContent = item.value;
    entry.append(label, value);
    list.appendChild(entry);
  });
}

function renderWorkItems(items) {
  const list = byId("workItems");
  list.replaceChildren();
  items.forEach((item) => {
    const entry = document.createElement("li");
    entry.textContent = item;
    list.appendChild(entry);
  });
}

function renderDocuments(items) {
  const list = byId("documentList");
  list.replaceChildren();
  items.forEach(([documentName, documentDetail, documentStatus]) => {
    const entry = document.createElement("article");
    entry.className = "document-item";
    const check = document.createElement("span");
    check.className = "document-check";
    check.setAttribute("aria-hidden", "true");
    check.textContent = "\u2713";
    const content = document.createElement("div");
    const name = document.createElement("strong");
    const detail = document.createElement("p");
    const status = document.createElement("span");
    name.textContent = documentName;
    detail.textContent = documentDetail;
    status.textContent = documentStatus;
    content.append(name, detail);
    entry.append(check, content, status);
    list.appendChild(entry);
  });
}

function renderTimeline(items) {
  const list = byId("reportTimeline");
  list.replaceChildren();
  items.forEach(([itemTime, itemEvent]) => {
    const entry = document.createElement("li");
    const time = document.createElement("time");
    const marker = document.createElement("i");
    const event = document.createElement("p");
    marker.setAttribute("aria-hidden", "true");
    time.textContent = itemTime;
    event.textContent = itemEvent;
    entry.append(time, marker, event);
    list.appendChild(entry);
  });
}

function renderAccess(items) {
  const list = byId("accessList");
  list.replaceChildren();
  items.forEach(([itemRecipient, itemDuration, itemPurpose]) => {
    const entry = document.createElement("article");
    entry.className = "access-item";
    const recipient = document.createElement("strong");
    const duration = document.createElement("span");
    const purpose = document.createElement("p");
    recipient.textContent = itemRecipient;
    duration.textContent = itemDuration;
    purpose.textContent = itemPurpose;
    entry.append(recipient, duration, purpose);
    list.appendChild(entry);
  });
}

function renderStatus(payload) {
  const valid = payload.receipt.integrity.valid;
  const integrity = byId("integrityStatus");
  integrity.textContent = valid ? copy("valid_unchanged") : copy("check_failed");
  integrity.className = `status ${valid ? "valid" : "invalid"}`;
  setText("localReceiptValue", valid ? copy("valid_local_signature") : copy("validation_failed"));

  const midnight = payload.midnight;
  const confirmed = midnight.status === "confirmed";
  const localizedLabel = locale.midnight.labels[midnight.status] || midnight.label;
  const localizedStatement = locale.midnight.statements[midnight.status] || midnight.statement;
  const status = byId("midnightStatus");
  status.textContent = localizedLabel;
  status.className = `status ${confirmed ? "confirmed" : "pending"}`;
  setText("networkProofTitle", localizedLabel);
  setText("midnightStatement", localizedStatement);
  setText("networkName", midnight.network || copy("not_submitted"));

  const transaction = midnight.transaction;
  byId("transactionFact").hidden = !transaction?.id;
  byId("blockFact").hidden = !transaction?.block_height && !transaction?.block_hash;
  if (transaction?.id) {
    const transactionId = byId("transactionId");
    transactionId.textContent = compactIdentifier(transaction.id, 12, 10);
    transactionId.title = transaction.id;
  }
  if (transaction?.block_height || transaction?.block_hash) {
    setText(
      "blockValue",
      transaction.block_height
        ? `#${transaction.block_height}`
        : compactIdentifier(transaction.block_hash, 10, 8),
    );
  }
}

function render(payload) {
  const sourceReport = payload.report;
  const report = locale.report;
  setText("demoNotice", copy("synthetic_notice"));
  setText("reportTitle", report.title);
  setText("reportSubtitle", report.subtitle);
  setText("packageReference", payload.receipt.package_id);
  setText("jobReference", sourceReport.job_reference);
  setText("reportVersion", `v${payload.receipt.version}`);
  setText("issuedAt", formatDate(payload.receipt.issued_at));
  setText("propertyReference", report.property_reference);
  setText("workPeriod", `${report.work_period.started} - ${report.work_period.completed}`);
  setText("reportSummary", report.summary);
  setText("deviations", report.deviations);
  setText("handoverNotes", report.handover_notes);
  setText("commitment", payload.receipt.commitment);
  renderParties(report.parties);
  renderWorkItems(report.work_items);
  renderTests(sourceReport.tests_and_results || []);
  renderDocuments(report.documents);
  renderTimeline(report.timeline);
  renderAccess(locale.access);
  renderStatus(payload);
}

async function loadReport({ announce = false } = {}) {
  const button = byId("verifyButton");
  button.disabled = true;
  try {
    const response = await fetch("/api/public/midnight-demo", {
      cache: "no-store",
      headers: { Accept: "application/json" },
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.message || copy("demo_unavailable"));
    render(payload);
    if (announce) {
      const verifiedMessage = payload.receipt.integrity.valid
        ? copy("package_verified_at").replace("{time}", formatVerificationTime())
        : copy("verification_failed");
      setText("verifiedAt", verifiedMessage);
    }
  } catch (error) {
    const integrity = byId("integrityStatus");
    integrity.textContent = copy("unavailable");
    integrity.className = "status invalid";
    setText("localReceiptValue", copy("unavailable"));
    setText("verifiedAt", error.message || copy("demo_unavailable"));
  } finally {
    button.disabled = false;
  }
}

applyLanguage();
byId("reportLanguage")?.addEventListener("change", (event) => {
  const nextLanguage = event.target.value;
  if (SUPPORTED_LANGUAGES.includes(nextLanguage)) {
    window.location.assign(`/${nextLanguage}/demo-report`);
  }
});
byId("verifyButton").addEventListener("click", () => loadReport({ announce: true }));
loadReport();
