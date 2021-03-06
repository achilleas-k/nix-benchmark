#include "nix.hpp"
#include <iostream>
#include <time.h>

using namespace nix;

std::vector<float> run(size_t N) {
    std::vector<float> times(N);
    nix::File file = nix::File::open("/tmp/data-benchmark.nix", nix::FileMode::Overwrite);
    nix::Block b = file.createBlock("test", "test");
    std::vector<double> data = std::vector<double>(N);
    for (size_t i = 0; i < N; i++) {
        std::string name = "times" + nix::util::numToStr(i);
        nix::DataArray da = b.createDataArray(name, "nix.event.positions", nix::DataType::Double, {1});
        const clock_t begin_time = clock();
        da.setData(data);
        times[i] = float(clock () - begin_time) /  CLOCKS_PER_SEC;
    }
    file.close();
    return times;
}


int main(int argc, char** argv){
    size_t N = atoi(argv[1]);
    std::vector<float> times = run(N);
    for (size_t i = 0; i < N; i++) {
        std::cout << i+1 << ", " << times[i] << std::endl;
    }
    return 0;
}
