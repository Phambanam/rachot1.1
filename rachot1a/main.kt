import java.io.File

fun doLifeBetter(inputName: String, output: String){
    val a = File(inputName).readLines()
    val result = mutableListOf<String>()

    for (i in a) {
        val ind = i.indexOf(']')
        if (ind != -1) {
            result.add(i.substring(ind + 1, i.length))
        } else result.add(i)
    }

    File(output).bufferedWriter().use {
        for (i in 0 until result.size) {
            it.write("[${i + 41}]" + result[i])
            it.newLine()
        }
    }
}

fun main(args: Array<String>) {
    print("d".indexOf('a'))
    doLifeBetter("C:\\Users\\judge\\Documents\\kek.txt", "outs.txt")
}