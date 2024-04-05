document.querySelectorAll(".chart-navigation-bar li").forEach(element => {
    element.addEventListener("click", (event)=>{
        selected_tab_data_attr = event.target.getAttribute("data-chart-variable");
        const other_tabs = document.querySelectorAll(`li[data-chart-variable]:not([data-chart-variable="${selected_tab_data_attr}"])`);
        other_tabs.forEach(other_tab => {
            other_tab.classList.remove("selected");
        });
        event.target.classList.add("selected");
    	const other_results = document.querySelectorAll(`.chart > div:not(.${selected_tab_data_attr})`);
    	other_results.forEach(other_result => {
            other_result.style.display = "none";
        });
        document.querySelectorAll(`.chart [data-chart-variable='${selected_tab_data_attr}']`)[0].style.display = "block";
    });
});