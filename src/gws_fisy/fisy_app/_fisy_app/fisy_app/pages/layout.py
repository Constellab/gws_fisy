import reflex as rx
from gws_reflex_base import get_theme

from ..state import State

app = rx.App(theme=get_theme())


def menu_item(icon: str, label: rx.Var, href: str) -> rx.Component:
    """Create a menu item with icon and label. Highlights when active.

    :param icon: The icon name (Lucide icon)
    :type icon: str
    :param label: The text label for the menu item
    :type label: rx.Var
    :param href: The URL to navigate to
    :type href: str
    :return: A menu item component
    :rtype: rx.Component
    """
    is_active = State.router.page.path == href

    return rx.link(
        rx.hstack(
            rx.icon(icon, size=20, flex_shrink="0"),
            rx.text(label, white_space="nowrap", overflow="hidden", text_overflow="ellipsis"),
            spacing="2",
            align="center",
            width="100%",
        ),
        href=href,
        width="100%",
        padding="0.75rem 1rem",
        border_radius="6px",
        background=rx.cond(is_active, "var(--accent-3)", "transparent"),
        color=rx.cond(is_active, "var(--accent-11)", "inherit"),
        font_weight=rx.cond(is_active, "600", "normal"),
        _hover={
            "background": rx.cond(is_active, "var(--accent-4)", "var(--gray-3)"),
        },
        text_decoration="none",
    )


def sidebar():
    """Create the sidebar navigation menu.

    :return: The sidebar component
    :rtype: rx.Component
    """
    i = State.i18n
    return rx.box(
        rx.vstack(
            # Header with app title
            rx.hstack(
                rx.icon("banknote", size=28, color="var(--accent-9)", flex_shrink="0"),
                rx.heading(State.app_title, size="6", line_height="1em", white_space="nowrap", overflow="hidden", text_overflow="ellipsis"),
                spacing="3",
                align="center",
                margin_bottom="1.5rem",
                width="100%",
            ),
            # Home
            menu_item("home", i["nav.home"], "/"),
            # Configuration
            menu_item("settings", i["nav.config"], "/config"),
            rx.divider(margin_y="0.5rem"),
            # Input section
            rx.text(i["nav.input"], weight="bold", size="2", color="var(--gray-11)", margin_bottom="0.25rem"),
            rx.vstack(
                menu_item("package", i["nav.activities"], "/input/activities"),
                menu_item("shopping_cart", i["nav.one_time"], "/input/one-time-sales"),
                menu_item("repeat", i["nav.subscriptions"], "/input/subscriptions"),
                menu_item("users", i["nav.staff"], "/input/staff"),
                menu_item("receipt", i["nav.charges"], "/input/external-charges"),
                menu_item("hard_drive", i["nav.investments"], "/input/investments"),
                menu_item("banknote", i["nav.funding"], "/input/funding"),
                width="100%",
                spacing="1",
                align_items="start",
            ),
            rx.divider(margin_y="0.5rem"),
            # Results section
            rx.text(i["nav.results"], weight="bold", size="2", color="var(--gray-11)", margin_bottom="0.25rem"),
            rx.vstack(
                menu_item("line_chart", i["nav.results.summary"], "/results/summary"),
                menu_item("file_bar_chart", i["nav.results.pnl"], "/results/income-statement"),
                menu_item("trending_up", i["nav.results.cashflow"], "/results/cashflow"),
                menu_item("wallet", i["nav.results.plan"], "/results/funding-plan"),
                menu_item("landmark", i["nav.results.balance"], "/results/balance-sheets"),
                width="100%",
                spacing="1",
                align_items="start",
            ),
            width="100%",
            align_items="start",
            padding="1.5rem",
        ),
        id="fisy-sidebar",
        width="280px",
        min_width="280px",
        max_width="280px",
        height="100vh",
        overflow_y="auto",
        position="fixed",
        top="0",
        left="0",
        flex_shrink="0",
        background="var(--color-background)",
        border_right="1px solid var(--gray-6)",
        z_index="100",
        custom_attrs={"data-sidebar": "fisy-sidebar"},
    )

def layout(content: rx.Component) -> rx.Component:
    """Main layout with sidebar and responsive content area.

    :param content: The main content component
    :type content: rx.Component
    :return: The complete layout
    :rtype: rx.Component
    """
    return rx.fragment(
        rx.script("""
            // Enhanced sidebar scroll position preservation
            (function() {
                const STORAGE_KEY = 'fisy-sidebar-scroll';
                const SIDEBAR_ID = 'fisy-sidebar';

                function getSidebar() {
                    return document.getElementById(SIDEBAR_ID);
                }

                function saveScrollPosition() {
                    const sidebar = getSidebar();
                    if (sidebar) {
                        sessionStorage.setItem(STORAGE_KEY, sidebar.scrollTop.toString());
                    }
                }

                function restoreScrollPosition() {
                    const sidebar = getSidebar();
                    const savedScroll = sessionStorage.getItem(STORAGE_KEY);
                    if (sidebar && savedScroll) {
                        // Use requestAnimationFrame to ensure DOM is ready
                        requestAnimationFrame(() => {
                            sidebar.scrollTop = parseInt(savedScroll, 10);
                        });
                    }
                }

                function attachScrollListener() {
                    const sidebar = getSidebar();
                    if (!sidebar || sidebar.dataset.scrollListenerAttached) return;

                    // Mark as attached to avoid duplicate listeners
                    sidebar.dataset.scrollListenerAttached = 'true';

                    // Save scroll position on scroll with debouncing
                    let scrollTimer;
                    sidebar.addEventListener('scroll', function() {
                        clearTimeout(scrollTimer);
                        scrollTimer = setTimeout(saveScrollPosition, 100);
                    }, { passive: true });

                    // Save immediately on link clicks
                    sidebar.addEventListener('click', function(e) {
                        if (e.target.closest('a')) {
                            saveScrollPosition();
                        }
                    }, true);
                }

                function init() {
                    attachScrollListener();
                    restoreScrollPosition();
                }

                // Initialize on DOM ready
                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', init);
                } else {
                    init();
                }

                // Re-initialize after Reflex navigation
                // Watch for changes in the body that indicate a page change
                let initTimer;
                const observer = new MutationObserver(function(mutations) {
                    // Debounce to avoid excessive calls
                    clearTimeout(initTimer);
                    initTimer = setTimeout(() => {
                        const sidebar = getSidebar();
                        if (sidebar && !sidebar.dataset.scrollListenerAttached) {
                            init();
                        } else if (sidebar) {
                            // Just restore position if sidebar exists
                            restoreScrollPosition();
                        }
                    }, 50);
                });

                observer.observe(document.body, {
                    childList: true,
                    subtree: true
                });

                // Also save on page unload
                window.addEventListener('beforeunload', saveScrollPosition);
            })();
        """),
        rx.box(
            sidebar(),
            rx.box(
                content,
                margin_left="280px",
                padding="0",
                max_width="100%",
                height="100vh",
                overflow_y="auto",
                display="flex",
                flex_direction="column",
            ),
            width="100%",
        ),
    )

def header_row(labels, widths=None):
    """Create table header row with optional fixed widths.

    :param labels: List of label components
    :type labels: list
    :param widths: Optional list of widths for columns
    :type widths: list | None
    :return: Table header component
    :rtype: rx.Component
    """
    if widths:
        return rx.table.header(
            rx.table.row(*[
                rx.table.column_header_cell(label, style={"width": w, "min_width": w})
                for label, w in zip(labels, widths, strict=True)
            ])
        )
    return rx.table.header(
        rx.table.row(*[rx.table.column_header_cell(label) for label in labels])
    )

def make_cell(comp: rx.Component, width: str = None):
    """Create table cell with optional fixed width.

    :param comp: The component to render in the cell
    :type comp: rx.Component
    :param width: Optional fixed width
    :type width: str | None
    :return: Table cell component
    :rtype: rx.Component
    """
    if width:
        return rx.table.cell(
            rx.box(comp, width="100%"),
            style={"width": width, "min_width": width}
        )
    return rx.table.cell(comp)


def table(rows, cols):
    """Simple table helper for displaying data tables"""
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.foreach(cols, lambda c: rx.table.column_header_cell(c))
            )
        ),
        rx.table.body(
            rx.foreach(
                rows,
                lambda r: rx.table.row(
                    rx.foreach(r, lambda cell: rx.table.cell(cell))
                )
            )
        ),
        style={"maxWidth": "100%", "overflowX": "auto"}
    )


def page_with_fixed_title(title: rx.Component, content: rx.Component) -> rx.Component:
    """Create a page layout with a fixed title at the top and scrollable content below.

    :param title: The title component (usually rx.heading)
    :type title: rx.Component
    :param content: The scrollable content below the title
    :type content: rx.Component
    :return: A box with fixed title and scrollable content
    :rtype: rx.Component
    """
    return rx.box(
        # Fixed title area
        rx.box(
            title,
            position="sticky",
            top="0",
            z_index="10",
            background="var(--color-background)",
            padding="2rem 2rem 1rem 2rem",
            border_bottom="1px solid var(--gray-6)",
        ),
        # Scrollable content area
        rx.box(
            content,
            padding="1rem 2rem 2rem 2rem",
            flex="1",
            overflow_y="auto",
        ),
        display="flex",
        flex_direction="column",
        height="100%",
        width="100%",
    )
