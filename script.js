const menuToggle = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#site-navigation");

function closeMenu(restoreFocus = false) {
  navigation.hidden = true;
  menuToggle.setAttribute("aria-expanded", "false");
  if (restoreFocus) menuToggle.focus();
}

closeMenu();
menuToggle.hidden = false;
document.documentElement.classList.add("navigation-ready");

menuToggle.addEventListener("click", () => {
  const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
  navigation.hidden = isOpen;
  menuToggle.setAttribute("aria-expanded", String(!isOpen));
});

navigation.addEventListener("click", (event) => {
  if (event.target.closest("a")) closeMenu();
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !navigation.hidden) closeMenu(true);
});

document.addEventListener("click", (event) => {
  if (!event.target.closest(".header-inner") && !navigation.hidden) closeMenu();
});

let stopActiveVideo;

document.querySelectorAll(".video").forEach((video) => {
  const link = video.querySelector(".video-poster");
  const stage = video.querySelector(".video-stage");
  const button = document.createElement("button");
  button.type = "button";
  button.className = link.className;
  button.setAttribute("aria-label", link.getAttribute("aria-label"));
  button.append(...link.childNodes);
  link.replaceWith(button);

  const close = document.createElement("button");
  close.type = "button";
  close.className = "close-video";
  close.textContent = "Close video";
  close.setAttribute("aria-label", `Close ${video.dataset.title}`);
  close.hidden = true;
  video.querySelector("figcaption").append(close);

  function stopVideo() {
    stage.querySelector("iframe")?.remove();
    button.hidden = false;
    close.hidden = true;
    stopActiveVideo = undefined;
  }

  close.addEventListener("click", () => {
    stopVideo();
    button.focus();
  });

  button.addEventListener("click", () => {
    stopActiveVideo?.();
    const frame = document.createElement("iframe");
    frame.src = `https://www.youtube-nocookie.com/embed/${video.dataset.video}?autoplay=1&rel=0&playsinline=1`;
    frame.title = video.dataset.title;
    frame.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
    frame.allowFullscreen = true;
    frame.referrerPolicy = "strict-origin-when-cross-origin";
    button.hidden = true;
    close.hidden = false;
    stage.append(frame);
    stopActiveVideo = stopVideo;
    frame.focus();
  });
});
