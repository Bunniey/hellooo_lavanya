const cards = [...document.querySelectorAll(".card")];
let current = 0;
function showCard(i){cards.forEach((card,idx)=>card.classList.toggle("active",idx===i))}
document.addEventListener("click",(e)=>{if(e.target.classList.contains("next-step")){current=Math.min(cards.length-1,current+1);showCard(current)}})
showCard(0);
