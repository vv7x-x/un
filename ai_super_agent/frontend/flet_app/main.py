import flet as ft
import httpx

API_BASE = "http://127.0.0.1:8000"


def themed_colors(theme: str):
    if theme == "cyberpunk":
        return {
            "bg": ft.colors.BLACK,
            "fg": ft.colors.LIME_300,
            "accent": ft.colors.PINK_300,
        }
    if theme == "golden":
        return {
            "bg": ft.colors.AMBER_50,
            "fg": ft.colors.AMBER_800,
            "accent": ft.colors.AMBER_400,
        }
    return {
        "bg": ft.colors.WHITE,
        "fg": ft.colors.BLACK,
        "accent": ft.colors.BLUE,
    }


def main(page: ft.Page):
    page.title = "AI Super Agent - Flet"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "auto"

    theme_dd = ft.Dropdown(options=[
        ft.dropdown.Option("official"),
        ft.dropdown.Option("cyberpunk"),
        ft.dropdown.Option("golden"),
    ], value="official")

    provider_dd = ft.Dropdown(options=[
        ft.dropdown.Option("ollama"),
        ft.dropdown.Option("openai"),
        ft.dropdown.Option("gemini"),
        ft.dropdown.Option("anthropic"),
    ], value="ollama")

    model_tf = ft.TextField(label="Model (optional)")
    prompt_tf = ft.TextField(label="Prompt", multiline=True, min_lines=5, max_lines=12, expand=True)
    output_tf = ft.TextField(label="Output", multiline=True, min_lines=10, max_lines=20, expand=True)

    async def apply_theme(_=None):
        colors = themed_colors(theme_dd.value)
        page.bgcolor = colors["bg"]
        prompt_tf.color = colors["fg"]
        output_tf.color = colors["fg"]
        provider_dd.color = colors["fg"]
        model_tf.color = colors["fg"]
        await page.update_async()

    async def run_complete(_):
        payload = {
            "prompt": prompt_tf.value,
            "provider": provider_dd.value,
            "model": model_tf.value or None,
        }
        output_tf.value = "Running..."
        await page.update_async()
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{API_BASE}/api/ai/complete", json=payload, timeout=60)
                data = resp.json()
                output_tf.value = data.get("text", "")
        except Exception as e:
            output_tf.value = str(e)
        await page.update_async()

    run_btn = ft.ElevatedButton("Complete", on_click=run_complete)
    theme_dd.on_change = apply_theme

    page.add(
        ft.Row([ft.Text("Theme"), theme_dd]),
        ft.Row([ft.Text("Provider"), provider_dd, model_tf, run_btn]),
        prompt_tf,
        output_tf,
    )

    page.on_resize = apply_theme
    page.on_view_pop = apply_theme

    page.update()


if __name__ == "__main__":
    ft.app(target=main)