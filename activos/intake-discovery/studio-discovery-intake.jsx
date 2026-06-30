import { useState, useCallback } from "react";

// ─── Design tokens ──────────────────────────────────────────────────────────────────────────────────────────────
// Palette: dark studio neutral base, electric teal accent, warm off-white text
// Type: system monospace for IDs/data, clean sans-serif for body
// Signature: vertical progress rail with live block labels — feels like a build log

const COLORS = {
  bg: "#0f1117",
  surface: "#181d27",
  surfaceHigh: "#1f2535",
  border: "#2a3349",
  borderActive: "#3dd6a3",
  accent: "#3dd6a3",
  accentDim: "#1a4a3a",
  text: "#e8edf5",
  textMuted: "#7a8aaa",
  textDim: "#4a5568",
  error: "#ff6b6b",
  warning: "#f6ad55",
  success: "#3dd6a3",
};

// ─── Schema ──────────────────────────────────────────────────────────────────────────────
const BLOQUES = [
  { id: "B0", label: "Contexto", icon: "◈" },
  { id: "B1", label: "Problema", icon: "⊙", critico: true },
  { id: "B2", label: "Criterio de éxito", icon: "◎", critico: true },
  { id: "B3", label: "Usuarios", icon: "◷" },
  { id: "B4", label: "Datos", icon: "⊞", critico: true },
  { id: "B5", label: "Integraciones", icon: "⊹" },
  { id: "B6", label: "Reglas de negocio", icon: "⊛" },
  { id: "B7", label: "Alcance", icon: "◈" },
];

const SISTEMAS = ["Gmail", "Google Sheets", "Google Drive", "Slack", "WhatsApp", "ERP", "CRM", "Notion", "Airtable", "Otro"];

const INITIAL_FORM = {
  modo: "",
  completado_por: "",
  tarea_dolor: "",
  proceso_actual: "",
  frecuencia: "",
  tiempo_por_vez: "",
  resultado_esperado: "",
  definicion_demo_ok: "",
  quien_usa: "",
  nivel_tecnico: "",
  entorno: [],
  origen_entrada: [],
  ejemplos_io: "",
  sistemas_conectar: [],
  herramientas_actuales: "",
  frustraciones: "",
  validaciones: "",
  revision_humana: "",
  revision_donde: "",
  mvp_minimo: "",
  datos_sensibles: "",
  volumen: "",
};

// ─── Helpers ──────────────────────────────────────────────────────────────────────────────
function generateId() {
  const ts = Date.now().toString(36).toUpperCase();
  const rand = Math.random().toString(36).slice(2, 5).toUpperCase();
  return `STD-${ts}-${rand}`;
}

function buildBrief(form, intakeId) {
  const fecha = new Date().toLocaleDateString("es-AR", { day: "2-digit", month: "2-digit", year: "numeric" });
  const entorno = form.entorno.join(", ") || "—";
  const origen = form.origen_entrada.join(", ") || "—";
  const sistemas = form.sistemas_conectar.join(", ") || "—";

  return `# Demo Brief — Studio Discovery
**Intake:** ${intakeId} · ${fecha} · Modo: ${form.modo || "—"} · Por: ${form.completado_por || "—"}

## 1. Problema y contexto
${form.tarea_dolor || "—"}

**Proceso actual:**
${form.proceso_actual || "—"}

**Frecuencia:** ${form.frecuencia || "—"} × ${form.tiempo_por_vez || "—"}

## 2. Criterio de éxito (Demo OK si…)
**Resultado esperado:** ${form.resultado_esperado || "—"}
**Definición de demo exitosa:** ${form.definicion_demo_ok || "—"}

## 3. Usuarios
**Quién usa:** ${form.quien_usa || "—"}
**Nivel técnico:** ${form.nivel_tecnico || "—"}
**Entorno:** ${entorno}

## 4. Datos — Entradas → Salidas
**Origen de entrada:** ${origen}
**Ejemplos reales:**
${form.ejemplos_io || "—"}

## 5. Integraciones
**Sistemas:** ${sistemas}
**Herramientas actuales:** ${form.herramientas_actuales || "—"}
**Frustraciones:** ${form.frustraciones || "—"}

## 6. Reglas de negocio
**Validaciones / Excepciones:** ${form.validaciones || "—"}
**Requiere revisión humana:** ${form.revision_humana || "—"}${form.revision_humana === "Sí" ? ` — Dónde: ${form.revision_donde || "—"}` : ""}

## 7. Alcance del MVP
**Mínimo demostrable:** ${form.mvp_minimo || "—"}
**Datos sensibles:** ${form.datos_sensibles || "—"}
**Volumen:** ${form.volumen || "—"}`;
}

// ─── Sub-components ───────────────────────────────────────────────────────────────────────
function Label({ children, required }) {
  return (
    <label style={{ display: "block", fontSize: 12, fontWeight: 600, letterSpacing: "0.08em", color: COLORS.textMuted, textTransform: "uppercase", marginBottom: 6 }}>
      {children}{required && <span style={{ color: COLORS.accent, marginLeft: 4 }}>*</span>}
    </label>
  );
}

function Input({ value, onChange, placeholder, multiline, rows = 3 }) {
  const base = {
    width: "100%", background: COLORS.bg, border: `1px solid ${COLORS.border}`,
    borderRadius: 6, color: COLORS.text, fontSize: 14, padding: "10px 12px",
    outline: "none", resize: multiline ? "vertical" : "none", fontFamily: "inherit",
    transition: "border-color 0.15s", boxSizing: "border-box",
  };
  const [focused, setFocused] = useState(false);
  const style = { ...base, borderColor: focused ? COLORS.borderActive : COLORS.border };

  return multiline
    ? <textarea value={value} onChange={e => onChange(e.target.value)} placeholder={placeholder}
        rows={rows} style={style} onFocus={() => setFocused(true)} onBlur={() => setFocused(false)} />
    : <input value={value} onChange={e => onChange(e.target.value)} placeholder={placeholder}
        style={style} onFocus={() => setFocused(true)} onBlur={() => setFocused(false)} />;
}

function Select({ value, onChange, options, placeholder }) {
  return (
    <select value={value} onChange={e => onChange(e.target.value)}
      style={{ width: "100%", background: COLORS.bg, border: `1px solid ${COLORS.border}`, borderRadius: 6, color: value ? COLORS.text : COLORS.textDim, fontSize: 14, padding: "10px 12px", outline: "none", fontFamily: "inherit", cursor: "pointer", boxSizing: "border-box" }}>
      <option value="" disabled>{placeholder}</option>
      {options.map(o => <option key={o} value={o}>{o}</option>)}
    </select>
  );
}

function ChipGroup({ options, selected, onChange }) {
  const toggle = (opt) => {
    const next = selected.includes(opt) ? selected.filter(x => x !== opt) : [...selected, opt];
    onChange(next);
  };
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
      {options.map(opt => {
        const active = selected.includes(opt);
        return (
          <button key={opt} onClick={() => toggle(opt)} style={{
            padding: "6px 12px", borderRadius: 20, fontSize: 13, cursor: "pointer", border: `1px solid`,
            borderColor: active ? COLORS.accent : COLORS.border,
            background: active ? COLORS.accentDim : "transparent",
            color: active ? COLORS.accent : COLORS.textMuted,
            transition: "all 0.15s",
          }}>{opt}</button>
        );
      })}
    </div>
  );
}

function RadioGroup({ options, value, onChange }) {
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
      {options.map(opt => {
        const active = value === opt;
        return (
          <button key={opt} onClick={() => onChange(opt)} style={{
            padding: "8px 16px", borderRadius: 6, fontSize: 13, cursor: "pointer", border: `1px solid`,
            borderColor: active ? COLORS.accent : COLORS.border,
            background: active ? COLORS.accentDim : "transparent",
            color: active ? COLORS.accent : COLORS.textMuted,
            transition: "all 0.15s",
          }}>{opt}</button>
        );
      })}
    </div>
  );
}

function ProgressRail({ current, total, bloques, modoVivo }) {
  const visibles = modoVivo ? [0, 1, 2, 4, 7] : bloques.map((_, i) => i);
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 0, paddingTop: 8 }}>
      {bloques.map((b, i) => {
        if (modoVivo && !visibles.includes(i)) return null;
        const visIdx = visibles.indexOf(i);
        const isCurrent = visIdx === current;
        const isDone = visIdx < current;
        return (
          <div key={b.id} style={{ display: "flex", alignItems: "flex-start", gap: 12, padding: "6px 0" }}>
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: 20 }}>
              <div style={{
                width: 20, height: 20, borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: 10, fontWeight: 700, border: "1.5px solid",
                borderColor: isDone ? COLORS.accent : isCurrent ? COLORS.accent : COLORS.border,
                background: isDone ? COLORS.accent : isCurrent ? COLORS.accentDim : "transparent",
                color: isDone ? COLORS.bg : isCurrent ? COLORS.accent : COLORS.textDim,
                transition: "all 0.2s",
              }}>{isDone ? "✓" : b.icon}</div>
              {visIdx < visibles.length - 1 && (
                <div style={{ width: 1, height: 24, background: isDone ? COLORS.accent : COLORS.border, marginTop: 2, transition: "background 0.2s" }} />
              )}
            </div>
            <div style={{ paddingTop: 1 }}>
              <div style={{ fontSize: 12, fontWeight: isCurrent ? 700 : 400, color: isCurrent ? COLORS.text : isDone ? COLORS.textMuted : COLORS.textDim, transition: "color 0.2s" }}>
                {b.label}
                {b.critico && <span style={{ marginLeft: 6, fontSize: 9, color: COLORS.accent, letterSpacing: "0.1em" }}>CLAVE</span>}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ─── Main ───────────────────────────────────────────────────────────────────────────────────
export default function StudioDiscovery() {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState(INITIAL_FORM);
  const [status, setStatus] = useState("idle"); // idle | sending | done | error
  const [brief, setBrief] = useState("");
  const [intakeId] = useState(generateId);

  const [briefTab, setBriefTab] = useState("brief"); // brief | json

  const modoVivo = form.modo === "En vivo";
  const visibleSteps = modoVivo ? [0, 1, 2, 4, 7] : [0, 1, 2, 3, 4, 5, 6, 7];
  const totalSteps = visibleSteps.length;
  const currentBloque = visibleSteps[step];

  const set = useCallback((key) => (val) => setForm(f => ({ ...f, [key]: val })), []);

  const canContinue = () => {
    switch (currentBloque) {
      case 0: return form.modo && form.completado_por;
      case 1: return form.tarea_dolor && form.proceso_actual;
      case 2: return form.resultado_esperado && form.definicion_demo_ok;
      case 3: return form.quien_usa;
      case 4: return form.ejemplos_io;
      case 5: return true;
      case 6: return form.revision_humana;
      case 7: return form.mvp_minimo;
      default: return true;
    }
  };

  const submitIntake = () => {
    setStatus("sending");
    const generatedBrief = buildBrief(form, intakeId);
    setBrief(generatedBrief);
    setStatus("done");
  };

  const renderBloque = () => {
    switch (currentBloque) {
      case 0:
        return (
          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            <div>
              <Label required>Modo de intake</Label>
              <RadioGroup value={form.modo} onChange={set("modo")}
                options={["En vivo", "Self-service"]} />
              <p style={{ fontSize: 12, color: COLORS.textDim, marginTop: 8 }}>
                <strong style={{ color: COLORS.textMuted }}>En vivo</strong> → 5 bloques clave, 10 min.&nbsp;&nbsp;
                <strong style={{ color: COLORS.textMuted }}>Self-service</strong> → todos los bloques, asíncrono.
              </p>
            </div>
            <div>
              <Label required>Completado por</Label>
              <RadioGroup value={form.completado_por} onChange={set("completado_por")}
                options={["Cliente", "Julio", "Ambos"]} />
            </div>
          </div>
        );

      case 1:
        return (
          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            <div>
              <Label required>¿Qué tarea te quita más tiempo hoy?</Label>
              <Input value={form.tarea_dolor} onChange={set("tarea_dolor")}
                placeholder="Ej: cargar facturas manualmente en el sistema cada mañana" />
            </div>
            <div>
              <Label required>Paso a paso de cómo se hace hoy</Label>
              <Input value={form.proceso_actual} onChange={set("proceso_actual")}
                placeholder="1. Abro el mail&#10;2. Descargo el adjunto&#10;3. Copio los datos a la planilla..." multiline rows={5} />
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
              <div>
                <Label>Frecuencia</Label>
                <Select value={form.frecuencia} onChange={set("frecuencia")}
                  placeholder="¿Cada cuánto?"
                  options={["Varias veces al día", "1 vez al día", "Varias veces a la semana", "1 vez a la semana", "Mensual"]} />
              </div>
              <div>
                <Label>Tiempo por vez</Label>
                <Select value={form.tiempo_por_vez} onChange={set("tiempo_por_vez")}
                  placeholder="¿Cuánto lleva?"
                  options={["< 5 min", "5–15 min", "15–30 min", "30–60 min", "+ de 1 hora"]} />
              </div>
            </div>
          </div>
        );

      case 2:
        return (
          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            <div>
              <Label required>¿Qué debe producir la herramienta?</Label>
              <ChipGroup
                options={["Reporte / PDF", "Email enviado", "Registro actualizado", "Archivo generado", "Notificación", "Dashboard", "Otro"]}
                selected={form.resultado_esperado ? [form.resultado_esperado] : []}
                onChange={vals => set("resultado_esperado")(vals[vals.length - 1] || "")} />
            </div>
            <div>
              <Label required>¿Cómo sabemos que la demo funcionó?</Label>
              <Input value={form.definicion_demo_ok} onChange={set("definicion_demo_ok")}
                placeholder="La demo funciona si... (sé específico: qué resultado concreto tiene que aparecer)"
                multiline rows={3} />
            </div>
          </div>
        );

      case 3:
        return (
          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            <div>
              <Label required>¿Quién va a usar la herramienta?</Label>
              <RadioGroup value={form.quien_usa} onChange={set("quien_usa")}
                options={["Solo yo", "Mi equipo", "Varios departamentos", "Clientes externos"]} />
            </div>
            <div>
              <Label>Nivel técnico de los usuarios</Label>
              <RadioGroup value={form.nivel_tecnico} onChange={set("nivel_tecnico")}
                options={["Básico", "Medio", "Avanzado", "Mixto"]} />
            </div>
            <div>
              <Label>¿Dónde la van a usar?</Label>
              <ChipGroup value={form.entorno} selected={form.entorno} onChange={set("entorno")}
                options={["Navegador web", "Celular", "Escritorio / app", "Dentro de otra plataforma"]} />
            </div>
          </div>
        );

      case 4:
        return (
          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            <div>
              <Label>¿De dónde salen los datos de entrada?</Label>
              <ChipGroup
                options={["Excel / Sheets", "Email", "Formulario web", "Base de datos", "Copiar-pegar manual", "PDF / archivo", "API externa", "Otro"]}
                selected={form.origen_entrada} onChange={set("origen_entrada")} />
            </div>
            <div>
              <Label required>2-3 ejemplos reales: entrada → salida esperada</Label>
              <Input value={form.ejemplos_io} onChange={set("ejemplos_io")}
                placeholder={"Ej 1:\nEntrada: mail con factura adjunta de Proveedor X, $15.000\nSalida: fila nueva en Sheet 'Facturas', columnas: proveedor, monto, fecha\n\nEj 2:\n..."}
                multiline rows={7} />
            </div>
          </div>
        );

      case 5:
        return (
          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            <div>
              <Label>¿Con qué sistemas debe conectarse?</Label>
              <ChipGroup options={SISTEMAS} selected={form.sistemas_conectar} onChange={set("sistemas_conectar")} />
            </div>
            <div>
              <Label>¿Qué herramientas usás hoy para esto?</Label>
              <Input value={form.herramientas_actuales} onChange={set("herramientas_actuales")}
                placeholder="Ej: Excel + email manual + copia a sistema interno" />
            </div>
            <div>
              <Label>¿Qué te frustra de esas herramientas?</Label>
              <Input value={form.frustraciones} onChange={set("frustraciones")}
                placeholder="Lo que más duele del proceso actual..." multiline rows={2} />
            </div>
          </div>
        );

      case 6:
        return (
          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            <div>
              <Label>¿Hay validaciones o reglas de negocio?</Label>
              <Input value={form.validaciones} onChange={set("validaciones")}
                placeholder="Ej: el monto no puede superar X, el campo Y es obligatorio, los martes no se procesan pagos..." multiline rows={3} />
            </div>
            <div>
              <Label required>¿Algún paso requiere aprobación o revisión humana?</Label>
              <RadioGroup value={form.revision_humana} onChange={set("revision_humana")}
                options={["Sí", "No", "Depende del caso"]} />
            </div>
            {(form.revision_humana === "Sí" || form.revision_humana === "Depende del caso") && (
              <div>
                <Label>¿En qué paso?</Label>
                <Input value={form.revision_donde} onChange={set("revision_donde")}
                  placeholder="Ej: antes de enviar el email al cliente, antes de actualizar el registro..." />
              </div>
            )}
          </div>
        );

      case 7:
        return (
          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            <div>
              <Label required>¿Qué mínimo tiene que funcionar para decir "esto sirve"?</Label>
              <Input value={form.mvp_minimo} onChange={set("mvp_minimo")}
                placeholder="Con que la demo haga X ya me convence. No necesito Y ni Z para esta primera versión."
                multiline rows={3} />
            </div>
            <div>
              <Label>¿Hay datos sensibles o restricciones de privacidad?</Label>
              <RadioGroup value={form.datos_sensibles} onChange={set("datos_sensibles")}
                options={["Sí", "No", "A revisar"]} />
            </div>
            <div>
              <Label>Volumen aproximado</Label>
              <Select value={form.volumen} onChange={set("volumen")}
                placeholder="¿Cuántos registros / operaciones?"
                options={["< 50 por día", "50–500 por día", "500–5.000 por día", "+ de 5.000 por día", "Variable / picos"]} />
            </div>
          </div>
        );

      default: return null;
    }
  };

  // ─── Done screen ───────────────────────────────────────────────────────────────────────
  if (status === "done") {
    const jsonOutput = JSON.stringify({ intake_id: intakeId, ...form }, null, 2);
    return (
      <div style={{ minHeight: "100vh", background: COLORS.bg, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "flex-start", padding: "40px 16px", fontFamily: "'Inter', system-ui, sans-serif" }}>
        <div style={{ width: "100%", maxWidth: 680 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
            <div style={{ width: 32, height: 32, borderRadius: "50%", background: COLORS.accent, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16 }}>✓</div>
            <div>
              <div style={{ color: COLORS.text, fontWeight: 700, fontSize: 18 }}>Brief generado</div>
              <div style={{ color: COLORS.textMuted, fontSize: 12, fontFamily: "monospace" }}>{intakeId}</div>
            </div>
          </div>

          <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
            {["brief", "json"].map(tab => (
              <button key={tab} onClick={() => setBriefTab(tab)} style={{
                padding: "6px 16px", borderRadius: 6, fontSize: 13, cursor: "pointer", border: `1px solid`,
                borderColor: briefTab === tab ? COLORS.accent : COLORS.border,
                background: briefTab === tab ? COLORS.accentDim : "transparent",
                color: briefTab === tab ? COLORS.accent : COLORS.textMuted,
              }}>{tab === "brief" ? "Brief Markdown" : "JSON"}</button>
            ))}
          </div>

          <div style={{ background: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: 10, padding: 20, maxHeight: 480, overflowY: "auto" }}>
            <pre style={{ color: COLORS.text, fontSize: 13, lineHeight: 1.7, whiteSpace: "pre-wrap", fontFamily: briefTab === "json" ? "monospace" : "inherit", margin: 0 }}>
              {briefTab === "brief" ? brief : jsonOutput}
            </pre>
          </div>

          <div style={{ display: "flex", gap: 10, marginTop: 16 }}>
            <button onClick={() => {
              navigator.clipboard.writeText(briefTab === "brief" ? brief : jsonOutput);
            }} style={{ flex: 1, padding: "12px 0", borderRadius: 8, border: `1px solid ${COLORS.border}`, background: "transparent", color: COLORS.textMuted, fontSize: 14, cursor: "pointer" }}>
              Copiar {briefTab === "brief" ? "brief" : "JSON"}
            </button>
            <button onClick={() => { setStep(0); setForm(INITIAL_FORM); setStatus("idle"); setBrief(""); }} style={{ flex: 1, padding: "12px 0", borderRadius: 8, border: "none", background: COLORS.accent, color: COLORS.bg, fontSize: 14, fontWeight: 700, cursor: "pointer" }}>
              Nuevo intake
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ─── Form screen ───────────────────────────────────────────────────────────────────────
  const bloque = BLOQUES[currentBloque];
  const isLast = step === totalSteps - 1;

  return (
    <div style={{ minHeight: "100vh", background: COLORS.bg, fontFamily: "'Inter', system-ui, sans-serif", display: "flex" }}>

      {/* Rail lateral */}
      <div style={{ width: 180, flexShrink: 0, padding: "32px 20px", borderRight: `1px solid ${COLORS.border}`, display: "flex", flexDirection: "column", gap: 0 }}>
        <div style={{ marginBottom: 24 }}>
          <div style={{ fontSize: 11, letterSpacing: "0.15em", color: COLORS.textDim, textTransform: "uppercase", marginBottom: 4 }}>Studio</div>
          <div style={{ fontSize: 15, fontWeight: 700, color: COLORS.text }}>Discovery</div>
          <div style={{ fontSize: 10, fontFamily: "monospace", color: COLORS.textDim, marginTop: 4 }}>{intakeId}</div>
        </div>
        <ProgressRail current={step} total={totalSteps} bloques={BLOQUES} modoVivo={modoVivo && step > 0} />
      </div>

      {/* Contenido */}
      <div style={{ flex: 1, padding: "40px 32px", maxWidth: 580, margin: "0 auto" }}>

        {/* Header del bloque */}
        <div style={{ marginBottom: 28 }}>
          <div style={{ fontSize: 11, letterSpacing: "0.12em", color: COLORS.accent, textTransform: "uppercase", marginBottom: 6 }}>
            {bloque.icon} {bloque.id}{bloque.critico ? " · Bloque clave" : ""}
          </div>
          <div style={{ fontSize: 22, fontWeight: 700, color: COLORS.text }}>{bloque.label}</div>
          <div style={{ marginTop: 6, height: 2, width: 32, background: COLORS.accent, borderRadius: 1 }} />
        </div>

        {/* Campos */}
        <div style={{ marginBottom: 32 }}>
          {renderBloque()}
        </div>

        {/* Navegación */}
        <div style={{ display: "flex", gap: 10 }}>
          {step > 0 && (
            <button onClick={() => setStep(s => s - 1)} style={{ padding: "12px 20px", borderRadius: 8, border: `1px solid ${COLORS.border}`, background: "transparent", color: COLORS.textMuted, fontSize: 14, cursor: "pointer" }}>
              ← Anterior
            </button>
          )}
          <button
            onClick={() => {
              if (isLast) { submitIntake(); }
              else { setStep(s => s + 1); }
            }}
            disabled={!canContinue() || status === "sending"}
            style={{
              flex: 1, padding: "12px 0", borderRadius: 8, border: "none",
              background: canContinue() ? COLORS.accent : COLORS.accentDim,
              color: canContinue() ? COLORS.bg : COLORS.textDim,
              fontSize: 14, fontWeight: 700, cursor: canContinue() ? "pointer" : "not-allowed",
              transition: "all 0.15s",
            }}>
            {status === "sending" ? "Enviando a Studio…" : isLast ? "Generar Brief →" : "Continuar →"}
          </button>
        </div>

        {/* Progress bar */}
        <div style={{ marginTop: 20, height: 2, background: COLORS.border, borderRadius: 1 }}>
          <div style={{ height: "100%", width: `${((step + 1) / totalSteps) * 100}%`, background: COLORS.accent, borderRadius: 1, transition: "width 0.3s" }} />
        </div>
        <div style={{ marginTop: 6, fontSize: 11, color: COLORS.textDim, textAlign: "right" }}>
          {step + 1} de {totalSteps}
        </div>
      </div>
    </div>
  );
}
