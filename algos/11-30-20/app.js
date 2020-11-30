let string = 'potato'

function reverseString(params) {
    let res = ''
    for (let i = 0, j = params.split('').length - 1; i < params.split('').length; i++, j--) {
        const el = params.split('')[j]
        if (el) {
            res += el
        }
    }
    return res

}

console.log(reverseString(string))