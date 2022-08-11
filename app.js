const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');
const movement = document.querySelector('#movement');
let flurry = []
flurry[0] = shot1 = new Bullets;
flurry[1] = shot2 = new Bullets;
flurry[2] = shot3 = new Bullets;
flurry[3] = shot4 = new Bullets;

canvas.width = 950;
game.height = 500;

let enemies = [];
const playerimg = new Image();
playerimg.src = './assets/plane.png';


//============================Start=====================//

window.addEventListener('DOMContentLoaded', function () {
    const runGame = this.setInterval(gameLoop, 60);
    spawnMob(enemies);
});


//============================Movements=================//
game.setAttribute('height', getComputedStyle(game)['height']);
game.setAttribute('width', getComputedStyle(game)['width']);


document.addEventListener('keydown', moveChar);

function moveChar(e) {


    switch (e.key) {

        //===================================Arrow cases for debugging purposes, no boundaries.
        // case 'ArrowUp':
        //     hero.y - 20 >= 0 ? (hero.y -= 20) : null;
        //     hero.frameY = 1;
        //     if (hero.frameX < hero.maxFrame) {
        //         hero.frameX++;
        //     } else { hero.frameX = hero.minFrame }
        //     break;
        // case 'ArrowLeft':
        //     hero.x - 20 >= 0 ? (hero.x -= 20) : null;
        //     hero.frameY = 2;
        //     if (hero.frameX < hero.maxFrame) {
        //         hero.frameX++;
        //     } else { hero.frameX = hero.minFrame }
        //     break;
        // case 'ArrowDown':
        //     hero.y + 20 <= game.height ? (hero.y += 20) : null;
        //     hero.frameY = 0;
        //     if (hero.frameX < hero.maxFrame) {
        //         hero.frameX++;
        //     } else { hero.frameX = hero.minFrame }
        //     break;
        // case 'ArrowRight':
        //     hero.x + 20 <= game.width ? (hero.x += 20) : null;
        //     hero.frameY = 3;
        //     if (hero.frameX < hero.maxFrame) {
        //         hero.frameX++;

        //     } else { hero.frameX = hero.minFrame }
        //     break;

        // WASD Keybindings

        case 'w':
            //can I stop all cases with one "if" conditional? ===== nope, one per case.
                hero.y - hero.speed >= 0 ? (hero.y -= hero.speed) : null;
                hero.frameY = 0;
                if (hero.frameX < hero.maxFrame) {
                    hero.frameX++;
                    hero.moving = true;
                }
            break;
        case 'a':
                hero.x - hero.speed >= 0 ? (hero.x -= hero.speed) : null;
                hero.frameY = 0;
                hero.frameX = 0;
            break;
        case 's':
                hero.y + hero.speed <= canvas.height ? (hero.y += hero.speed) : null;
                hero.frameY = 1;
                if (hero.frameX < hero.maxFrame) {
                    hero.frameX++;
                    hero.moving = true;
                }
            break;
        case 'd':
                hero.x + hero.speed <= canvas.width ? (hero.x += hero.speed) : null;
                hero.frameY = 0;
                hero.frameX = 0;
            break;
        //ADDITIONAL CONTROLS
        case 'e':
            break;
        case ' ':
            spacebar();
    }
}


//==================Loop=============//


function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    movement.textContent = `x:${hero.x}\ny:${hero.y}`;

    // ctx.drawImage(bg, 0, 0);
    
    hero.render();
    hero.draw();
    enemies[0].spawn();
    fire();
    endFire();
    bulletOrigin();
}

//=====================Useful functions =================//

