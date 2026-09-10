/* Campaign persistence: one browser, one run. Separate key from the quiz journal; never converts quiz entries.
   save() writes then reads back and confirms the revision; load() returns {state, saved_at} or null, or {error}.
   A stale tab is detected by comparing the stored revision with the one in memory before applying a command. */
(function (root) {
  const KEY = 'stockgame.campaign.v1';
  function load() {
    try { const raw = localStorage.getItem(KEY); if (!raw) return null; const j = JSON.parse(raw); if (!j || !j.state || typeof j.state.revision !== 'number') return { error: 'The saved campaign could not be read.' }; return j; }
    catch (e) { return { error: 'The saved campaign could not be read: ' + e.message }; }
  }
  function save(state) {
    try {
      const payload = { state, saved_at: new Date().toISOString(), key_version: 1 };
      localStorage.setItem(KEY, JSON.stringify(payload));
      const back = JSON.parse(localStorage.getItem(KEY) || 'null');
      return !!(back && back.state && back.state.revision === state.revision && back.state.clock.date === state.clock.date);
    } catch (e) { return false; }
  }
  function storedRevision() { const j = load(); return j && j.state ? j.state.revision : null; }
  function clear() { try { localStorage.removeItem(KEY); } catch (e) {} }
  function exportText() { try { return localStorage.getItem(KEY) || ''; } catch (e) { return ''; } }
  root.CAMPAIGN_STORE = { KEY, load, save, storedRevision, clear, exportText };
})(window);
