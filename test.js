
function checkExpressiosn(str) {

    const stack = []

    if (!str) {
        return false
    }

    for (let i = 0; i < str.length; i++) {
        if (str[i] === '(' || str[i] === '{' || str[i] === '[') {
            stack.push(str[i])
        }

        if (str[i] === ')' || str[i] === '}' || str[i] === ']') {
            if (stack.length === 0) {
                return false
            }

            let removed = stack.pop()

            if (removed === '(' && str[i] != ')') {
                return false
            }
            if (removed === '[' && str[i] != ']') {
                return false
            }
            if (removed === '{' && str[i] != '}') {
                return false
            }

        }
    }
    if (stack.length > 0) {
        return false
    }

    return true

}
