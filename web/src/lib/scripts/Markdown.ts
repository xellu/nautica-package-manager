import { createHighlighter } from 'shiki'
import { marked } from 'marked'
import markedShiki from 'marked-shiki'
import DOMPurify from 'dompurify'


let highlighter: any = null

async function getHighlighter() {
    if (!highlighter) {
        highlighter = await createHighlighter({
            themes: ['catppuccin-mocha'],
            langs: ['python', 'typescript', 'javascript', 'bash', 'toml', 'json']
        })
    }
    return highlighter
}

async function parseMarkdownRaw(markdown: string): Promise<string> {
    const highlighter = await getHighlighter()
    
    marked.use(markedShiki({
        highlight(code, lang) {
            return highlighter.codeToHtml(code, {
                lang: lang || 'text',
                theme: 'catppuccin-mocha'
            })
        }
    }))
    
    return marked.parse(markdown)
}

export async function parseMarkdown(markdown: string): Promise<string> {
    const raw = await parseMarkdownRaw(markdown);
    return DOMPurify.sanitize(raw)
}