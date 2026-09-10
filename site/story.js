/* Dated editorial feedback. Date-only sources must precede an opening-price exit.
   A retrospective source unlocks at publication, not at the event it describes. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.STORY = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  function lastDay(date) {
    if (/^\d{4}-\d{2}-\d{2}$/.test(date || '')) return date;
    if (/^\d{4}-\d{2}$/.test(date || '')) {
      const [y, m] = date.split('-').map(Number);
      return new Date(Date.UTC(y, m, 0)).toISOString().slice(0, 10);
    }
    return null;
  }
  function availableBefore(event, exit) {
    const occurred = lastDay(event.date), published = lastDay(event.source && event.source.published);
    return !!(occurred && published && occurred < exit && published < exit);
  }
  function atExit(outcome, exit) {
    const authored = outcome.scene_check && outcome.scene_check.dated_debrief;
    if (!authored) return null;
    const events = (outcome.aftermath && outcome.aftermath.events || []).filter(e => availableBefore(e, exit));
    const byId = new Map(events.map(e => [e.id, e]));
    const checks = Object.fromEntries(Object.entries(authored.baseline.checks).map(([id, text]) => [id, { text, event_ids: [] }]));
    let narrative = { text: authored.baseline.narrative, event_ids: [] };
    const updates = authored.updates.filter(u => u.event_ids.length && u.event_ids.every(id => byId.has(id)))
      .sort((a, b) => {
        const latest = u => u.event_ids.map(id => {
          const e = byId.get(id); return [lastDay(e.date), lastDay(e.source.published)].sort().pop();
        }).sort().pop();
        return latest(a).localeCompare(latest(b));
      });
    for (const u of updates) {
      if (u.narrative) narrative = { text: u.narrative, event_ids: u.event_ids };
      for (const [id, text] of Object.entries(u.checks || {})) checks[id] = { text, event_ids: u.event_ids };
    }
    return { events, checks, narrative, stops: (outcome.scene_check.walkthrough || []).filter(s => byId.has(s.event.id)) };
  }
  return { availableBefore, atExit };
});
