import { useState, useEffect } from "react";
import { X, Key, CheckCircle2, AlertCircle, Eye, EyeOff, ExternalLink, Trash2, Sparkles } from "lucide-react";
import { motion, AnimatePresence } from "motion/react";
import { useBridge } from "../hooks/useBridge";

interface SettingsModalProps {
  open: boolean;
  onClose: () => void;
}

export function SettingsModal({ open, onClose }: SettingsModalProps) {
  const bridge = useBridge();

  const [apiKey, setApiKey] = useState("");
  const [showKey, setShowKey] = useState(false);
  const [configured, setConfigured] = useState<boolean | null>(null);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  // Load status when modal opens
  useEffect(() => {
    if (!open || !window.pybridge) return;
    bridge
      .call<{ configured: boolean }>("getApiKeyStatus")
      .then((res) => setConfigured(res?.configured ?? false));
  }, [open]); // eslint-disable-line react-hooks/exhaustive-deps

  const flash = (type: "success" | "error", text: string) => {
    setMessage({ type, text });
    setTimeout(() => setMessage(null), 4000);
  };

  const handleSave = async () => {
    if (!apiKey.trim()) return;
    setSaving(true);
    const res = await bridge.call<{ configured: boolean }>("saveApiKey", apiKey.trim());
    setSaving(false);
    if (res?.configured) {
      setConfigured(true);
      setApiKey("");
      flash("success", "API key saved to OS keychain. AI features are now active.");
    } else {
      flash("error", "Could not save the key — check the format (should start with sk-ant-).");
    }
  };

  const handleClear = async () => {
    const res = await bridge.call<{ configured: boolean }>("clearApiKey");
    if (res !== null) {
      setConfigured(false);
      flash("success", "API key removed from secure storage.");
    }
  };

  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-black/50 backdrop-blur-sm"
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.96, y: 16 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: 16 }}
            transition={{ type: "spring", duration: 0.35 }}
            className="relative w-full max-w-lg bg-card border border-border rounded-2xl shadow-2xl overflow-hidden"
          >
            {/* Header */}
            <div className="flex items-center justify-between px-6 py-5 border-b border-border">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center">
                  <Sparkles className="w-4 h-4 text-blue-400" />
                </div>
                <div>
                  <h2 className="text-base font-semibold">Settings</h2>
                  <p className="text-xs text-muted-foreground">Claude AI integration</p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-1.5 hover:bg-accent rounded-lg text-muted-foreground hover:text-foreground transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="p-6 space-y-6">
              {/* Status banner */}
              <div className={`flex items-center gap-3 px-4 py-3 rounded-xl border ${
                configured
                  ? "bg-emerald-500/10 border-emerald-500/20"
                  : "bg-muted/30 border-border"
              }`}>
                {configured ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-500 flex-shrink-0" />
                ) : (
                  <AlertCircle className="w-5 h-5 text-muted-foreground flex-shrink-0" />
                )}
                <div>
                  <p className={`text-sm font-medium ${configured ? "text-emerald-500" : "text-foreground"}`}>
                    {configured ? "AI features active" : "AI features not configured"}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {configured
                      ? "Your API key is stored securely in the OS keychain."
                      : "Add your Anthropic API key to enable task breakdown, capture, and weekly insights."}
                  </p>
                </div>
              </div>

              {/* What AI unlocks */}
              {!configured && (
                <div className="space-y-2">
                  <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    What you unlock
                  </p>
                  {[
                    { icon: "✦", text: "Break any task into subtasks with one click" },
                    { icon: "✦", text: "Paste notes or emails → extract action items" },
                    { icon: "✦", text: "AI-written weekly productivity digest" },
                  ].map((f) => (
                    <div key={f.text} className="flex items-center gap-2.5 text-sm text-muted-foreground">
                      <span className="text-blue-400 text-xs">{f.icon}</span>
                      {f.text}
                    </div>
                  ))}
                </div>
              )}

              {/* API key input */}
              <div className="space-y-2">
                <label className="flex items-center gap-2 text-sm font-medium">
                  <Key className="w-3.5 h-3.5 text-muted-foreground" />
                  {configured ? "Replace API Key" : "Enter API Key"}
                </label>
                <div className="relative">
                  <input
                    type={showKey ? "text" : "password"}
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSave()}
                    placeholder="sk-ant-api03-..."
                    autoComplete="off"
                    spellCheck={false}
                    className="w-full pl-4 pr-10 py-2.5 bg-input-background rounded-xl border border-border text-sm font-mono focus:outline-none focus:ring-2 focus:ring-ring"
                  />
                  <button
                    type="button"
                    onClick={() => setShowKey((v) => !v)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                    tabIndex={-1}
                    aria-label={showKey ? "Hide key" : "Show key"}
                  >
                    {showKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                <p className="text-xs text-muted-foreground">
                  Stored in the OS keychain — never written to disk in plaintext.
                </p>
              </div>

              {/* Flash message */}
              <AnimatePresence>
                {message && (
                  <motion.div
                    initial={{ opacity: 0, y: -4 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    className={`text-sm px-4 py-2.5 rounded-xl ${
                      message.type === "success"
                        ? "bg-emerald-500/10 text-emerald-500 border border-emerald-500/20"
                        : "bg-destructive/10 text-destructive border border-destructive/20"
                    }`}
                  >
                    {message.text}
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Actions */}
              <div className="flex items-center gap-3 pt-1">
                <button
                  onClick={handleSave}
                  disabled={!apiKey.trim() || saving}
                  className="flex-1 py-2.5 bg-blue-500 text-white rounded-xl text-sm font-medium hover:bg-blue-600 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                >
                  {saving ? "Saving…" : "Save API Key"}
                </button>
                {configured && (
                  <button
                    onClick={handleClear}
                    className="flex items-center gap-2 px-4 py-2.5 border border-destructive/30 text-destructive hover:bg-destructive/10 rounded-xl text-sm transition-colors"
                    title="Remove key from keychain"
                  >
                    <Trash2 className="w-4 h-4" />
                    Remove
                  </button>
                )}
              </div>

              {/* Get API key link */}
              <div className="flex items-center justify-center pt-1">
                <a
                  href="https://console.anthropic.com/settings/keys"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors"
                >
                  <ExternalLink className="w-3 h-3" />
                  Get your API key from console.anthropic.com
                </a>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
