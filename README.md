# masonre-artifacts

Public host for masonre's shareable HTML artifacts — interactive maps, apps, and one-off tools.

## How to publish something

1. Drop your `.html` file in this repo (root or any folder).
2. Commit and push:

   ```bash
   git add . && git commit -m "Add <name>" && git push
   ```

3. Wait a minute or two for GitHub Pages to deploy.
4. Share the public URL:

   ```
   https://masonre21.github.io/masonre-artifacts/<filename>.html
   ```

Files in folders work too: `maps/houston.html` becomes `.../masonre-artifacts/maps/houston.html`.

## Brief

Shareable link analyzer:

```
https://masonre21.github.io/masonre-artifacts/link-brief.html
```

Paste a YouTube or website URL → get a summary, product/service link, pricing, and reviews, then answer whether you want to sign up. The page also includes a Cursor Automation prompt so you can repeat the same workflow from Cursor.

## Notes

- Everything in this repo is **public** — do not commit anything with client-confidential data.
- The index page at the root URL lists nothing by default; only people with a direct link will find a file easily, but it is still public.
