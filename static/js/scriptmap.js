const labels = document.querySelectorAll("text");

labels.forEach((label) => {
  label.addEventListener("mouseover", () => {
    const code = label.getAttribute("class");
    const elements = document.querySelectorAll(`.${code}`);

    for (const element of elements) {
      if (element.tagName !== "text") element.classList.add("hover");
    }
  });

  label.addEventListener("mouseleave", () => {
    const elements = document.querySelectorAll(`.hover`);

    for (const element of elements) {
      element.classList.remove("hover");
    }
  });
});

const palette = {
  background: "#2c3e50",
  land: "#f4a261",
  secondary: "#92613a",
  text: "#ffffff",
};

function applyPalette(palette) {
  const styles = `
    text {
      fill: ${palette.text};
    }

    #background {
      fill: ${palette.background};
    }

    .landxx {
      fill: ${palette.land};
      stroke: ${palette.secondary};
    }

    g:hover path,
    path:hover,
    path.hover,
    g.hover path {
      fill: ${palette.secondary};
    }
  `;

  const paletteStyle = document.getElementById("palette");
  paletteStyle?.remove();

  document.body.style.backgroundColor = palette.background;

  const svg = document.querySelector("#svg-map");
  const style = document.createElement("style");

  svg.prepend(style);
  style.setAttribute("id", "palette");

  style.appendChild(document.createTextNode(styles));
}

window.onload = function () {
  applyPalette(palette);
};

const labelsSwitch = document.getElementById("show-labels");

labelsSwitch.addEventListener("change", (e) => {
  const labels = document.getElementById("labels");
  labels.style.display = e.target.checked ? "block" : "none";
});

document
  .getElementById("downloadButton")
  .addEventListener("click", function () {
    const svgContent = new XMLSerializer().serializeToString(
      document.querySelector("#svg-map")
    );

    const blob = new Blob([svgContent], { type: "image/svg+xml" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "SVG World Map with labels.svg";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });
