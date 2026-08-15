// Make the desktop nav-cluster dropdowns (Product / Updates / Company)
// mutually exclusive: opening one closes the others.
//
// The <details> elements already share `name="cosmos-nav-cluster"`, which
// modern browsers (Chromium 120+) treat as a native exclusive-accordion
// group -- opening one auto-closes its named siblings with no JS at all.
// This script is a defensive fallback for browsers that don't yet honor
// shared `name` on <details>: it's idempotent alongside native support
// (if native already closed a sibling, setting its already-false `open`
// to false again is a no-op) and stays keyboard-accessible, because the
// `toggle` event fires identically for a click and for a keyboard
// Enter/Space activation on a focused <summary> -- no separate keyboard
// handling needed.
document.querySelectorAll('.cosmos-nav-group').forEach(function (group) {
  group.addEventListener('toggle', function () {
    if (!group.open) return;
    document.querySelectorAll('.cosmos-nav-group').forEach(function (other) {
      if (other !== group) other.open = false;
    });
  });
});

// Click-outside and Escape close any open dropdown cluster. Keeps the
// one-at-a-time behavior above intact -- this only ever needs to close,
// never open, a group.
function closeOpenNavGroups() {
  document.querySelectorAll('.cosmos-nav-group[open]').forEach(function (group) {
    group.open = false;
  });
}

document.addEventListener('click', function (e) {
  // Never intercept a link's own click -- this handler only ever *closes*
  // a dropdown, but a closed <details> hides its content, and closing the
  // group the clicked link lives in out from under it (synchronously,
  // before the browser gets to the link's default navigate action) is
  // exactly the kind of thing that can eat a click. Belt-and-suspenders:
  // bail out on any <a href> click, not just clicks inside a nav group.
  if (e.target.closest('a[href]')) return;
  if (e.target.closest('.cosmos-nav-group')) return;
  closeOpenNavGroups();
});

document.addEventListener('keydown', function (e) {
  if (e.key !== 'Escape') return;
  closeOpenNavGroups();
});
