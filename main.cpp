#include <memory>
#include <iostream>
#include <vector>

#include <boost/timer/timer.hpp>
#include <mapnik/geometry.hpp>
#include <mapnik/wkt/wkt_factory.hpp>

// geos
#include <geos_c.h>

int main( int argc, char** argv)
{
    initGEOS(0,0);

    if (argc < 2)
    {
        std::cerr << "Usage:" << argv[0] << " <wkt> [<num_runs>=1000]" << std::endl;
        return EXIT_FAILURE;
    }

    std::string wkt(argv[1]);
    unsigned NUM_RUNS = 1000;
    if (argc == 3)
    {
        NUM_RUNS = std::atoi(argv[2]);
    }

    std::cerr << wkt << std::endl;
    std::cerr << "Parsing ^^ " << NUM_RUNS << " times." << std::endl;
    for (int k=0; k<2;++k)
    {
        {
            std::cerr << "GEOS wkt-parser" << std::endl;
            boost::timer::auto_cpu_timer t;
            unsigned count = 0;
            GEOSWKTReader * reader = GEOSWKTReader_create();
            if (reader)
            {
                for (unsigned i = 0; i < NUM_RUNS; ++i)
                {

                    GEOSGeometry* geometry = GEOSWKTReader_read(reader, wkt.c_str());
                    if (geometry)
                    {
                        ++count;
                        GEOSGeom_destroy(geometry);
                    }
                }
            }
            GEOSWKTReader_destroy(reader);
            std::cerr << "count=" << count << std::endl;
        }
        {
            std::cerr << "MAPNIK wkt-parser" << std::endl;
            boost::timer::auto_cpu_timer t;
            unsigned count = 0;
            mapnik::wkt_parser parser;
            for (unsigned i = 0; i < NUM_RUNS; ++i)
            {
                boost::ptr_vector<mapnik::geometry_type> geom;
                if (parser.parse(wkt , geom))
                    //if (mapnik::from_wkt(wkt , geom))
                    ++count;
            }
            std::cerr << "count=" << count << std::endl;
        }
    }
    return EXIT_SUCCESS;
}
