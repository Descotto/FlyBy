//===================Space=================//


//================Ships Class========//
class Ships {
    constructor() {
        this.x = 0;
        this.y = 229;
        this.width = 80;
        this.height = 16;
        this.moving = false;
        this.speed = 5;
        this.frwidth = 65;
        this.frheight = 75;
        this.frameX = 0;
        this.frameY = 0;
        this.maxFrame = 2;
        this.image = '';
        this.drawSprite = function (img, sX, sY, sW, sH, dX, dY, dW, dH) {
            ctx.drawImage(img, sX, sY, sW, sH, dX, dY, dW, dH);
        }
        this.draw = function () {
            this.drawSprite(playerimg, this.frwidth * this.frameX, this.frheight * this.frameY, this.frwidth, this.frheight, this.x + 10, this.y - 20, this.frwidth, this.frheight);

        }
        this.render = function () {
            ctx.strokeStyle = 'white'
            ctx.strokeRect(hero.x, hero.y, this.width, this.height);
        }
    }
}
//====================Cube Fighters ======//
class Cube {
    constructor() {
        this.x = 500;
        this.y = 229;
        this.width = 50;
        this.height = 50;
        this.spawn = function () {
            ctx.strokeStyle = 'white'
            ctx.strokeRect(this.x, this.y, this.width, this.height);
        }
    }
}
//==================Bullets -- will make sense laater====//
class Bullets {
    constructor() {
        this.x = 110;
        this.y = 229;
        this.width = 10;
        this.height = 10;
        this.speed = 7;
        this.active = false;
        this.shoot = function() {
            ctx.strokeStyle = 'white';
            ctx.strokeRect(this.x, this.y, this.width, this.height);

        }
    }
}

//============Some Functions========//
//======== detect hit =======////
//=== if obj1 touches obj2 it returns true
function detechHit(obj1, obj2) {
    let hitBox =
        obj1.y + obj1.height > obj2.y &&
        obj1.y < obj2.y + obj2.height &&
        obj1.x + obj1.width > obj2.x &&
        obj1.x < obj2.x + obj2.width;

    if (hitBox) {
        return true;
    } else {
        return false;
    }
}
//======= lazers and shuchs.
function fire(){
   flurry.forEach(element => {
    if (element.active) {
        element.shoot();
        element.x += 25
    }
   })
}
function endFire() {
    flurry.forEach(element => {
        enemies.forEach(enemy => {
        if (detechHit(element, enemy) || element.x >= canvas.width) {
            element.active = false;
            element.x = 110;
    }})})
}

//============ Monitor and adjust bullet orogins======= //
function bulletOrigin() {
    flurry.forEach(element => {
        if (element.active == false) {
            element.x = hero.x + 110;
            element.y = hero.y;
        }
    })
}
//tie it to spacebarr
function spacebar() {
    let i = 0;
    flurry.forEach(element => {
        i++;
        if (i === 3 || i === 0) {
            element.active = true;
        }
        if (i > 10){
            i = 0;
        }
        
});
}
//============== lazy functions ===//
function spawnMob(array){
    for (let i = 0; i < 5; i++) {
        if (i < 5) {
            array[i] = new Cube;
        }else {
            console.log(array);
        }
    }
}
let hero =  new Ships;
let shot = new Bullets;