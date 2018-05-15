import numpy as np
from intern.remote.boss import BossRemote
from intern.resource.boss.resource import ChannelResource, ExperimentResource, CoordinateFrameResource

class NeuroDataResource:
    def __init__(self, host, token, collection, experiment):
        self._bossRemote = BossRemote({'protocol': 'https',
                                       'host': host,
                                       'token': token})
        self.collection = collection
        self.experiment = experiment
        self.channels = self._bossRemote.list_channels(collection, experiment)
        self.channels.remove('empty') #Delete "empty" channel
        self._get_coord_frame_details()


    def _get_coord_frame_details(self):
        exp_resource = ExperimentResource(self.experiment, self.collection)
        coord_frame = self._bossRemote.get_project(exp_resource).coord_frame

        coord_frame_resource = CoordinateFrameResource(coord_frame)
        data = self._bossRemote.get_project(coord_frame_resource)

        self.max_dimensions = (data.z_stop, data.y_stop, data.x_stop)
        self.voxel_size = (data.z_voxel_size, data.y_voxel_size, data.x_voxel_size)


    def _get_channel(self, chan_name):
        """
        Helper that gets a fully initialized ChannelResource for an *existing* channel.
        Args:
            chan_name (str): Name of channel.
            coll_name (str): Name of channel's collection.
            exp_name (str): Name of channel's experiment.
        Returns:
            (intern.resource.boss.ChannelResource)
        """
        chan = ChannelResource(chan_name, self.collection, self.experiment)
        return self._bossRemote.get_project(chan)

    def assert_channel_exists(self, channel):
        return channel in self.channels

    def get_cutout(self, chan, zRange=None, yRange=None, xRange=None):
        if chan not in self.channels:
            print('Error: Channel Not Found in this Resource')
            return
        if zRange is None or yRange is None or xRange is None:
            print('Error: You must supply zRange, yRange, xRange kwargs in list format')
            return

        channel_resource = self._get_channel(chan)
        datatype = channel_resource.datatype

        data = self._bossRemote.get_cutout(channel_resource,
                                           0,
                                           xRange,
                                           yRange,
                                           zRange)

        return data

    @staticmethod
    def ingest_volume(host, token, channel_name, collection, experiment, volume):
        """
        Assumes the collection and experiment exists in BOSS.
        """
        
        remote = BossRemote({'protocol': 'https',
                             'host': host,
                             'token': token})

        if volume.dtype == 'uint64':
            dtype = 'uint64'
            img_type = 'annotation'
            sources = ['empty']
        else:
            dtype = volume.dtype.name
            img_type = 'image'
            sources = []
        
        try:
            channel_resource = ChannelResource(channel_name, collection, experiment)
            channel = remote.get_project(channel_resource)
        except:
            channel_resource = ChannelResource(channel_name, collection, experiment,
                                               type=img_type,
                                               sources=sources,
                                               datatype=dtype)
            channel = remote.create_project(channel_resource)

        #Get max size of experiment
        exp_resource = ExperimentResource(experiment, collection)
        coord_frame = remote.get_project(exp_resource).coord_frame
        coord_frame_resource = CoordinateFrameResource(coord_frame)
        data = remote.get_project(coord_frame_resource)
        y_stop, x_stop = data.y_stop, data.x_stop
        
        for z in range(volume.shape[0]):
            print('Uploading {} slice'.format(z))
            remote.create_cutout(channel,
                                 0,
                                 (0, x_stop), 
                                 (0, y_stop),
                                 (z, z + 1), 
                                 volume[z, :, :].reshape((-1, y_stop, x_stop)))

        

"""
def test_function():
    #load ground truth file
    gt = io.imread('./data/gt.tiff')

    #api token is stored externally for security
    token = pickle.load(open('./data/token.pkl', 'rb'))
    host = 'api.boss.neurodata.io'
    myResource = NeuroDataResource(host,
                                  token,
                                  'collman',
                                  'collman15v2',
                                  [{'name':'annotation', 'dtype':'uint64'},
                                   {'name':'DAPI1st', 'dtype':'uint8'},
                                   {'name':'GABA488', 'dtype':'uint8'}])

    cutout = myResource.get_cutout('annotation', [2,4], [2300,2500], [3400,3700])

    print(gt.shape == cutout.shape)
    print(delta_epsilon(np.mean(gt), np.mean(cutout), 1e-4))


if __name__ == '__main__':
    test_function()
"""
