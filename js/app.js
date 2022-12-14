// https://github.com/darkreader/darkreader/issues/4342#issuecomment-791334982
(
    head = document.querySelector('head'),
    handleMutation = () => (
      darkreaderSelector = 'meta[name="darkreader"]',
      darkreaderActive = (head.querySelector(darkreaderSelector) != null),
      document.body.classList.toggle('dark-reader', darkreaderActive)
    ),
    handleMutation(),
    new MutationObserver(handleMutation).observe(head, { childList: true })
);