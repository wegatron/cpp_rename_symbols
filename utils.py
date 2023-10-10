import os

#base_dir = '/home/wegatron/win-data/workspace/ces_adk/research/'
base_dir = '/Users/zhangshengwei/workspace/ces_adk/'

# 不进行扫描的目录
skip_files = [
    'makefile',
    '/build/',
    '/sample/',
    '/test/',
    '/examples/',
    '/external/',
    '/third_party/',
    '/3rd/',
    'kiwi/backend_ext/',
    'amcomdef.h',
    'amstring.h',
    'ammem.h',
    'amplat.h',
    'amstream.h',
    'amdisplay.h',
    'qvcomdef.hpp',
    'qvglutils.hpp',
    'qvar3DSceneManager.h',
    'vtpxjsonreader.h',
    'xyrdg/header/data.h',
    'kiwi/utils/half.h'    
]

# 扫描该目录下的符号, 排除这些符号
exclude_dirs = [
    'include/3Dcube',
    'include/RenderEngine',
    'include/animationtext',
    'include/atom3d_engine',
    'include/bling',
    'include/color_curve',
    'include/common',
    'include/common_source',
    'include/effect',
    'include/et3dstream',
    'include/etaecomposition',
    'include/etdistributestream',
    'include/eteffecttemplateutils',
    'include/etfacegradualchangestream',
    'include/etfacestream',
    'include/etlayerStylestream',
    'include/etparticlegpustream',
    'include/etpenoutputstream',
    'include/etripplestream',
    'include/etsaberstream',
    'include/etsubeffectstreamfactory',
    'include/etsubstream',
    'include/etvg2dstream',
    'include/facedetector',
    'include/glsl_optimizer',
    'include/hair_flow',
    'include/kiwi',
    'include/liblsfacewarp',
    'include/libqvar',
    'include/libqvblur',
    'include/libqvlayerStyle',
    'include/libqvmeshWarp',
    'include/libqvripple',
    'include/libqvsaber',
    'include/libvtfx',
    'include/libxyfacegradualchange',
    'include/mesh_warp',
    'include/motion_tile',
    'include/opengles',
    'include/particlestream',
    'include/particlesystem',
    'include/particlesystemgpu',
    'include/qvae',
    'include/qvmorphing',
    'include/qvpen',
    'include/screencapturesession',
    'include/shatter',    
    'research/vtpathfx/source/kernel/cJSON',
    'research/AtomEngine2/header/math',
    'research/AtomEngine2/header/utils',
    'research/AtomEngine2/external',
    'research/AtomEngine2/engine/glTF',
    'research/AtomEngine2/header/glTF'
]

search_dirs = [        
        'research/libqvar',
        'research/libqvblur',
        'research/libqvlayerstyle',
        'research/libqvshatter',
        'research/libqvmeshWarp',
        'research/libqvsaber',
        'research/libxyfacegradualchange',
        'research/vt2d',
        'research/vtpathfx',
        'research/kiwi',
        'research/xyvap',
        'research/AtomEngine2',
        'include/shatter',  
]

def isSkip(file_path):
    for ec in skip_files:
        if file_path.find(ec) != -1:
            return True
    return False

def isExclude(file_path):
    for ec in exclude_dirs:
        if file_path.find(ec) != -1:
            return True
    return False

def traverse_directory(logger, directory, search_extensions, visit, restart_file):
    begin_flag = len(restart_file) == 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Construct the full path of the file
            file_path = os.path.join(root, file)

            if isSkip(file_path):
                #logger.info(f'skip: {file_path}')
                continue

            if (begin_flag or file_path == restart_file):
                begin_flag = True
                file_extension = file_path[file_path.rfind('.'):]
                if file_extension in search_extensions:
                    visit(file_path)
