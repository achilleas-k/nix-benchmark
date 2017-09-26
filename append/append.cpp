#include "nix.hpp"
#include <iostream>
#include <time.h>

using namespace nix;

float append(nix::Block &block, nix::Group &group, size_t count) {
    float time;
    nix::DataArray da = block.createDataArray("times" + nix::util::numToStr(count), "nix.event.positions", nix::DataType::Double, {1});

    const clock_t begin_time = clock();
    group.addDataArray(da);
    time = float( clock () - begin_time ) /  CLOCKS_PER_SEC;
    return time;
}


std::vector<float> run(size_t N) {
    std::vector<float> times(N);
    nix::File file = nix::File::open("/tmp/append-benchmark.nix", nix::FileMode::Overwrite);
    nix::Block b = file.createBlock("test", "test");
    nix::Group g = b.createGroup("group", "timing_test");
    for (size_t i = 0; i < N; i++) {
        times[i] = append(b, g, i);
    }
    file.close();
    return times;
}


int main(int argc, char** argv){
    /* size_t N = 100; */
    size_t N = atoi(argv[1]);
    std::vector<float> times = run(N);
    float sum = 0.0;
    for (size_t i = 0; i < N; i++) {
        sum += times[i];
        std::cout << i+1 << ", " << sum << std::endl;
    }
    /* std::cerr << sum << std::endl; */

    return 0;
}
