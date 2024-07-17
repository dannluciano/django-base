function setupTheme() {
	// THEMES
	const STORAGE_KEY = "bulma-theme";
	const SYSTEM_THEME = "system";
	const DEFAULT_THEME = "light";

	const state = {
		chosenTheme: SYSTEM_THEME, // light|dark|system
		appliedTheme: DEFAULT_THEME, // light|dark
		OSTheme: null, // light|dark|null
	};

	const updateThemeUI = () => {
		switch (state.chosenTheme) {
			case "light":
				themeSwitcher.textContent = "🌑";
				break;
			case "dark":
				themeSwitcher.textContent = "💻";
				break;
			case "system":
				themeSwitcher.textContent = "🌞";
				break;
			default:
				break;
		}
	};

	const themeSwitcher = document.getElementById("theme-switcher");
	themeSwitcher.addEventListener("click", (event) => {
		console.log(state.chosenTheme);
		switch (state.chosenTheme) {
			case "light":
				setTheme("dark");
				break;
			case "dark":
				setTheme("system");
				break;
			case "system":
				setTheme("light");
				break;
			default:
				break;
		}
	});

	const setTheme = (theme, save = true) => {
		state.chosenTheme = theme;
		state.appliedTheme = theme;

		if (theme === SYSTEM_THEME) {
			state.appliedTheme = state.OSTheme;
			document.documentElement.removeAttribute("data-theme");
			window.localStorage.removeItem(STORAGE_KEY);
		} else {
			document.documentElement.setAttribute("data-theme", theme);

			if (save) {
				window.localStorage.setItem(STORAGE_KEY, theme);
			}
		}

		updateThemeUI();
	};

	const toggleTheme = () => {
		if (state.appliedTheme === "light") {
			setTheme("dark");
		} else {
			setTheme("light");
		}
	};

	const detectOSTheme = () => {
		if (!window.matchMedia) {
			// matchMedia method not supported
			return DEFAULT_THEME;
		}

		if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
			// OS theme setting detected as dark
			return "dark";
		}
		if (window.matchMedia("(prefers-color-scheme: light)").matches) {
			return "light";
		}

		return DEFAULT_THEME;
	};

	// On load, check if any preference was saved
	const localTheme = window.localStorage.getItem(STORAGE_KEY);
	state.OSTheme = detectOSTheme();

	if (localTheme) {
		setTheme(localTheme, false);
	} else {
		setTheme(SYSTEM_THEME);
	}

	window
		.matchMedia("(prefers-color-scheme: dark)")
		.addEventListener("change", (event) => {
			const theme = event.matches ? "dark" : "light";
			state.OSTheme = theme;
			setTheme(theme);
		});
}

document.addEventListener("DOMContentLoaded", setupTheme);
document.body.addEventListener("htmx:afterSwap", setupTheme);
