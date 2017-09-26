#include "nix.hpp"
#include <iostream>
#include <time.h>

using namespace nix;


float run_test(size_t n) {
    nix::File file = nix::File::open("data-benchmark.nix", nix::FileMode::Overwrite);
    nix::Block b = file.createBlock("test", "test");
    std::vector<double> data = std::vector<double>(n);
    std::string name = "times" + nix::util::numToStr(n);
    const clock_t begin_time = clock();
    nix::DataArray da = b.createDataArray(name, "nix.event.positions", nix::DataType::Double, {1});
    da.setData(data);
    float time = float(clock () - begin_time) /  CLOCKS_PER_SEC;
    file.close();
    return time;
}


int main(int argc, char** argv){
    /* size_t N = 100; */
    size_t N = atoi(argv[1]);
    float t;
    for (size_t n = 0; n < N; n++) {
        t = run_test(N);
        std::cout << n+1 << ", " << t << std::endl;
    }
    return 0;
}
