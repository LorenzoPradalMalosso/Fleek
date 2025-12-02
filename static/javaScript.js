// Botões do menu
const btnPlaylist = document.getElementById("btn-playlist");
const btnSearch   = document.getElementById("btn-search");
const btnProfile  = document.getElementById("btn-profile");
const btnTheme    = document.getElementById("btn-theme");

// Exemplo de ações
btnPlaylist.onclick = () => alert("Abrir playlists...");
btnSearch.onclick   = () => alert("Abrir pesquisa...");
btnProfile.onclick  = () => alert("Abrir perfil...");

// Modo escuro/claro (exemplo simples)
btnTheme.onclick = () => {
  document.body.classList.toggle("light");
};
