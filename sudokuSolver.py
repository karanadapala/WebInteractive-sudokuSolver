from selenium import webdriver
import time
import numpy as np
from selenium.webdriver.common.keys import Keys

def possible(x,y,n, grid):
    for index in range(9):
        if (grid[x][index] == n) or (grid[index][y]==n):
            return False
    xo = int(x/3)*3
    yo = int(y/3)*3
    for xx in range(xo,xo+3):
        for yy in range(yo,yo+3):
            if grid[xx][yy]==n:
                return False
    return True

def preFillrows(preFillD):
    global driver
    for preFillnum in range(1,10):
        for preFillsplit in range(3):
            preFillCount = 0
            tempx =3*preFillsplit
            tempy = 3*preFillsplit+3
            matColindex = 0
            for preFillx in range(tempx, tempy):
                if preFillnum in preFillD[preFillx]:
                    preFillCount += 1
                    matColindex -= int(preFillD[preFillx].index(preFillnum)/3)
                else:
                    tempz = preFillx
            matCol = 3 + matColindex
            if preFillCount == 2:
                preFillCal = 0
                for preFilly in range(matCol*3,matCol*3+3):
                    if preFillD[tempz][preFilly] == 0:
                        if possible(tempz,preFilly,preFillnum, preFillD):
                            preFillCal += 1
                            fillx = tempz
                            filly = preFilly
                if preFillCal==1:
                    preFillD[fillx][filly] = preFillnum
                    driver.find_element_by_id('f{}{}'.format(filly,fillx)).send_keys('{}'.format(preFillnum))
    return preFillD

def preFillcols(preFillD):
    global driver
    for preFillnum in range(1,10):
        for preFillsplit in range(3):
            preFillCount = 0
            tempx =3*preFillsplit
            tempy = 3*preFillsplit+3
            
            for preFillx in range(tempx, tempy):
                matRowindex = 0

                for temprow in range(9):
                    if preFillnum == preFillD[temprow][preFillx]:
                        preFillCount += 1
                        matRowindex +=0
                if matRowindex== 0:
                    tempz = preFillx
            tempz = int(tempz/3)*3
            if preFillCount == 2:
                preFillCal = 0
                for preFilly in range(9):
                    for preFilltemp in range(tempz, tempz+3):
                        
                        if preFillD[preFilly][preFilltemp] == 0:
                            if possible(preFilly,preFilltemp,preFillnum, preFillD):
                                preFillCal += 1
                                filly = preFilltemp
                                fillx = preFilly
                if preFillCal==1:
                    preFillD[fillx][filly] = preFillnum
                    driver.find_element_by_id('f{}{}'.format(filly,fillx)).send_keys('{}'.format(preFillnum))
    return preFillD

def postPrefill(preFillD,cnt):
    for postPrefillnum in range(1,10):
        for postx in range(3):
            xIndex = postx*3
            for posty in range(3):
                yIndex=posty*3
                postPrefillCount = 0
                for subMatx in range(xIndex, xIndex+3):
                    
                    for subMaty in range(yIndex, yIndex+3):
                        if preFillD[subMatx][subMaty]==0:
                            if possible(subMatx,subMaty,postPrefillnum, preFillD):
                                #print(postPrefillnum, subMatx, subMaty)
                                postPrefillCount +=1
                                tempX = subMatx
                                tempY = subMaty
                if postPrefillCount == 1:
                    print(postPrefillnum,tempX, tempY)
                    preFillD[tempX][tempY] = postPrefillnum
                    driver.find_element_by_id('f{}{}'.format(tempY,tempX)).send_keys('{}'.format(postPrefillnum))
    preFillcols(preFillD)
    preFillrows(preFillD)
    preFillcols(preFillD)
    preFillrows(preFillD)
    c = 0
    kar = preFillD
    for kk in preFillD:
        if 0 not in kk:
            c += len(kk)
    if c == 81:
        return preFillD
    cnt += 1
    if kar==preFillD or cnt > 150:
        return preFillD
    time.sleep(10)
    postPrefill(preFillD, cnt)
    
    
    
                        



def solve(grid):
    global driver
    for solx in range(9):
        for soly in range(9):
            if grid[solx][soly] == 0:
                for num in range(1,10):
                    if possible(solx,soly, num, grid):
                        grid[solx][soly] = num
                        driver.find_element_by_id('f{}{}'.format(soly,solx)).send_keys('{}'.format(num))
                        solve(grid)
                        count = 0
                        for tt in grid:
                            if 0 not in tt:
                                count += len(tt)
                            if count == 81:
                                return
                        grid[solx][soly] = 0
                        driver.find_element_by_id('f{}{}'.format(soly,solx)).send_keys(Keys.BACKSPACE)
                return
    #print(np.matrix(grid))
    
        
if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path='../Trading_bot/chromedriver_linux64/chromedriver')
    difficulty = input('difficulty level (1 to 4) ?: ')
    driver.get('https://nine.websudoku.com/?level={}'.format(difficulty))
    d = []
    time.sleep(1)
    for i in range(9):
        temp = []
        for j in range(9):
            try:
                elem = driver.find_element_by_id('f{}{}'.format(j,i)).get_attribute('value')
                if elem == '':
                    elem = 0
            except:
                elem=0
            temp.append(int(elem))
        d.append(temp)


    for k in d:
        print(k)
    print('-----solution-----')
    
    kar =[]
    xcount = 0
    while kar != d:
        kar = d
        preFillrows(d)
        preFillcols(d)
        preFillrows(d)
        preFillcols(d)
        postPrefill(d,xcount)
    #time.sleep(20)
    # x = int(difficulty)*10
    # for mm in range(x):
        
    #     postPrefill(d)
    #     preFillrows(d)
    #     preFillcols(d)
    #     c=0
    #     for kk in d:
    #         if 0 not in kk:
    #             c += len(kk)
    #     if c == 81:
    #         break
    
    postPrefill(d,xcount)
    np.matrix(d)
    print('reccccc')
    solve(d)
    
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/table/tbody/tr[2]/td/form/p[4]/input[1]').click()

    time.sleep(10)
    driver.close()