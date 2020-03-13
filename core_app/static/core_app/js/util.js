
class Util {

    constructor () {
        const convertDay = {
            0: 'Sun',
            1: 'Mon',
            2: 'Tue',
            3: 'Wed',
            4: 'Thu',
            5: 'Fri',
            6: 'Sat'
        }

        const convertMonth = {
            0: 'Jan',
            1: 'Feb',
            2: 'Mar',
            3: 'Apr',
            4: 'May',
            5: 'Jun',
            6: 'July',
            7: 'Aug',
            8: 'Sep',
            9: 'Oct',
            10: 'Nov',
            11: 'Dec',
        }

        const intervals = {
            w: 604800,
            d: 86400,
            h: 3600,
            m: 60,
            s: 1
        }
    }

    getBetweenDates (startDate, stopDate) {
        let dateArray = new Array();
        let currentDate = startDate;
        
        while (currentDate <= stopDate) {
            dateArray.push({
                day: this.convertDay[currentDate.getDay()],
                date: `${currentDate.getDate()}/${this.convertMonth[currentDate.getMonth()]}`
            })
            currentDate = currentDate.addDays(1);
        }

        return dateArray;
    }

    convertSecondToTime (second) {
        let result = '';
        second = Number.parseInt(second);

        Object.keys(intervals).forEach(function(key) {
            let value = Number.parseInt(second/intervals[key]);
            if (value !== 0) {
                second -= value*intervals[key]
                result+=`${value}${key}`
            }
        });

        if (result.length === 0) {
            return '0m';
        }

        return result;
    }
}

export default Util;