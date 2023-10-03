import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {#練習3 キーと移動量の対応関係の辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

def chack_bound(obj_rct: pg.Rect):
    """
    引数:こうかとんRect OR ばくだんRect
    戻り値:タプル(横方向判定結果 縦方向判定結果)
    画面内ならTrue,画面外ならFalse
    """
    yoko = True
    tate = True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: # 横方向判定
        yoko = False 
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: # 縦方向判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400) # 練習3 こうかとんの初期座標の設定
    """ばくだん"""
    bd_img = pg.Surface((20, 20))#爆弾の生成
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)#爆弾の生成
    bd_rct = bd_img.get_rect() #Rectの取得
    x, y = random.randint(0, WIDTH), random.randint(0,HEIGHT)#移動範囲の指定
    bd_rct.center = (x, y)
    vx, vy = +5, +5 

    """ばくだん2"""
    bd2_img = pg.Surface((20, 20))#爆弾の生成
    bd2_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd2_img, (255, 0, 0), (10, 10), 10)#爆弾の生成
    bd2_rct = bd2_img.get_rect() #Rectの取得
    x2, y2 = random.randint(0, WIDTH), random.randint(0,HEIGHT)#移動範囲の指定
    bd2_rct.center = (x2, y2)
    vx2, vy2 = +5, +5 


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        screen.blit(bg_img, [0, 0])
        
        if kk_rct.colliderect(bd_rct) or kk_rct.colliderect(bd2_rct): # 練習5 + 演習5 ぶつかった判定
            print("game over")
            kk_img = pg.image.load("ex02/fig/8.png") # 演習3 泣いてる画像の読み込み
            kk_img = pg.transform.rotozoom(kk_img, 0, 2.0) 
            screen.blit(kk_img,kk_rct)
            pg.display.update()
            time.sleep(3) # 演習3 時間の停止
            return
                       
        

        """こうかとん"""
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in delta.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] # 練習3 縦方向の合計移動量
                sum_mv[1] += mv[1] # 練習3 横方向の合計移動量
        kk_rct.move_ip(sum_mv[0], sum_mv[1]) # 練習3 移動
        if chack_bound(kk_rct) != (True, True): # 練習4 はみ出し判定
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])



        screen.blit(kk_img, kk_rct) # 練習3 移動後の表示
        
        """ばくだん"""
        screen.blit(bd_img, bd_rct) #練習1
        bd_rct.move_ip(vx, vy)
        yoko, tate = chack_bound(bd_rct)
        if not yoko: # 練習4 横方向の判定
            vx *= -1
        if not tate: # 練習4 縦方向の判定
            vy *= -1

        """ばくだん２"""
        if tmr >= 100: # 演習5 時間経過による2つ目のばくだんの追加
            screen.blit(bd2_img, bd2_rct) #練習1
            bd2_rct.move_ip(vx2, vy2)
            yoko2, tate2 = chack_bound(bd2_rct)
            if not yoko2: # 演習5 横方向の判定
                vx2 *= -1
            if not tate2: # 演習5 縦方向の判定
                vy2 *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()