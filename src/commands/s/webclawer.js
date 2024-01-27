import puppeteer from 'puppeteer';
import { useAppStore } from '@/store/app'

const webclawer = async(inputname) => {
    
    const appStore = useAppStore()
    
    // Launch the browser & init setting
    const browser = await puppeteer.launch({headless: "new"});
    const page = await browser.newPage();
    await page.setViewport({width: 1080*1.5, height: 1024});
    await page.goto(`https://www.tradingview.com/chart/?symbol=${inputname}`, {waitUntil: 'networkidle0'});

    // screenshoting the stock chart
    const chart = await page.waitForSelector('body > div.js-rootresizer__contents.layout-with-border-radius > div.layout__area--center');
    await chart.screenshot({path: `@/../screenshot/${inputname}.png`});
    await chart.dispose();

    // creating the stock name
    const name = await page.waitForSelector('body > div.js-rootresizer__contents.layout-with-border-radius > div.layout__area--center > div.chart-container.single-visible.top-full-width-chart.active > div.chart-container-border > div > div.chart-markup-table > div:nth-child(1) > div.chart-markup-table.pane > div > div.legend-l31H9iuA.noWrap-l31H9iuA.wrappable-l31H9iuA > div.legendMainSourceWrapper-l31H9iuA > div.item-l31H9iuA.series-l31H9iuA > div.noWrapWrapper-l31H9iuA > div.titlesWrapper-l31H9iuA > div.titleWrapper-l31H9iuA.mainTitle-l31H9iuA.apply-overflow-tooltip.apply-common-tooltip.withAction-l31H9iuA.withDot-l31H9iuA > div.title-l31H9iuA');
    const stockname = await name.evaluate(el => el.textContent);
    appStore.ChartName = stockname
    //console.log(typeof appStore.webdetail)
    console.log(appStore.ChartName)
    await name.dispose();

    // creating the stock icon
    const icon = await page.waitForSelector('body > div.js-rootresizer__contents.layout-with-border-radius > div.layout__area--center > div.chart-container.single-visible.top-full-width-chart.active > div.chart-container-border > div > div.chart-markup-table > div:nth-child(1) > div.chart-markup-table.pane > div > div.legend-l31H9iuA.noWrap-l31H9iuA.wrappable-l31H9iuA > div.legendMainSourceWrapper-l31H9iuA > div.item-l31H9iuA.series-l31H9iuA > div.noWrapWrapper-l31H9iuA > div.titlesWrapper-l31H9iuA > div.titleWrapper-l31H9iuA.mainTitle-l31H9iuA.apply-overflow-tooltip.apply-common-tooltip.withAction-l31H9iuA.withDot-l31H9iuA > div.logoWrapper-l31H9iuA > span:nth-child(2) > img');
    //await icon.screenshot({path: `screenshot/icon${num}.png`});
    const iconsrc = await icon.evaluate(img => img.src);
    //console.log(iconsrc)

    const page2 = await browser.newPage();
    await page2.setViewport({width: 18, height: 18});
    await page2.goto(iconsrc, {waitUntil: 'networkidle0'});
    await page2.screenshot({path: `@/../screenshot/icon${inputname}.png`});

    await browser.close();
}

export default webclawer;
