#include <iostream>
#include <fstream>
#include <map>

struct Word
{
    char* data_;

    Word() //explicit
    {
    }

    Word(char* data)  //explicit
    {
        data_ = data; //content?
    }

    ~Word()
    {
        delete data_; //no allocating
        data_ = 0; //after deleting?
    }

    bool operator<(Word y) //const &
    {
        return data_ < y.data_; //comparing pointers?
    }
};

std::map<Word, int> freqMap; 

int main(int argc, char* argv[])
{
    auto fileName = argv[1]; //argc is unused; what if there is no second argument?

    std::fstream file(fileName); //is writing really needed?

    char c;

    do
    {
        do { c = file.get(); } while (c == ' ');

        file.put(c); //put to the next character? why writing to file?

        char* buf = new char[64]; //magic number

        for (int i = 0; i < 64; ++i)
        {
            buf[i] = file.get();
            if (buf[i] == ' ') //add '\0'
                break;
        }

        do { c = file.get(); } while (c == ' ');

        Word w(buf);

        if (freqMap.count(w) != 0) //is it more likely?
            freqMap[w] = freqMap[w] + 1; 
        else
            freqMap[w] = 0;

        //delete [] buf;
    } while (file.good()); //file.good() will be checked only after trying to run the code inside block

    for (auto p : freqMap) //& to avoid copying
        std::cout << p.first.data_ << " = " << p.second;

    return 0;
}
