using NetTopologySuite.Geometries;
using OSMLSGlobalLibrary;
using OSMLSGlobalLibrary.Map;
using OSMLSGlobalLibrary.Modules;

namespace airportSimulation {
    public class TestModule : OSMLSModule {
        // Тестовая точка.
        Point point;

        // Тестовая линия.
        LineString line;

        // Тестовый полигон.
        Polygon polygon;

        // Тестовый "самолет".
        Airplane airplane;

        protected override void Initialize() {
            #region создание базовых объектов
            // (Следует обратить внимание, что все координаты у всех геометрических объектов задаются в сферической проекции Меркатора (EPSG:3857).)
            // Создание координаты точки в начале координат.
            var pointCoordinate = new Coordinate(0, 0);
            // Создание стандартной точки в созданных ранее координатах.
            point = new Point(pointCoordinate);

            // Создание координат для линии.
            var lineCoordinates = new Coordinate[] {
                point.Coordinate,
                new Coordinate(0, -2000000),
                new Coordinate(-3000000, -1500000)
            };
            // Создание стандартной кривой линии по ранее созданным координатам.
            line = new LineString(lineCoordinates);

            // Создание координат полигона.
            var polygonCoordinates = new Coordinate[] {
                    new Coordinate(4000000, 5000000),
                    new Coordinate(6000000, 0),
                    new Coordinate(6000000, 6000000),
                    new Coordinate(4000000, 5000000)
            };
            // Создание стандартного полигона по ранее созданным координатам.
            polygon = new Polygon(new LinearRing(polygonCoordinates));

            #endregion

            #region создание базовых объектов

            // Добавление созданных объектов в общий список, доступный всем модулям. Объекты из данного списка отображаются на карте.
            MapObjects.Add(point);
            MapObjects.Add(line);
            MapObjects.Add(polygon);

            #endregion

            #region создание кастомного объекта и добавление на карту, модификация полигона заменой точки

            // Координаты самолёта, сконвертированные из Lat/Lon координат. Примерно в аэропорту "Internacional de Carrasco".
            var airplaneCoordinate = MathExtensions.LatLonToSpherMerc(-34.831747, -56.020034);
            // Скорость самолета, опять же, в сферической проекции Меркатора.
            var airplaneSpeed = 1000;
            // Создание объекта класса "самолет", реализованного в рамках данного модуля.
            airplane = new Airplane(airplaneCoordinate, airplaneSpeed);
            // Добавление самолета в список объектов.
            MapObjects.Add(airplane);

            // Заменим одну из точек ранее созданного полигона только что созданным самолетом.
            polygonCoordinates[2] = airplaneCoordinate;

            #endregion

            #region демонстрация получения данных из коллекции MapObjects
            // Коллекция MapObjects нужна не только для хранения и отображения объектов, но ещё и для удобного доступа к ним.

            // Попробуем получить все объекты, являющиеся строго точками.
            var onlyPoints = MapObjects.Get<Point>(); // Будет возвращена точка, созданная в самом начале.

            // А теперь получим все объекты, являющиеся точками и наследующиеся от точек (а также наследников наследников).
            var allPoints = MapObjects.GetAll<Point>(); // Будет возвращена точка, созданная в самом начале и самолет.

            // А теперь получим ВСЕ объекты на карте.
            var allMapObjects = MapObjects.GetAll<Geometry>(); // Будут возвращены все 4 созданных нами объекта.

            #endregion
        }

        /// <summary>
        /// Вызывается постоянно, здесь можно реализовывать логику перемещений и всего остального, требующего времени.
        /// </summary>
        /// <param name="elapsedMilliseconds">TimeNow.ElapsedMilliseconds</param>
        public override void Update(long elapsedMilliseconds) {
            // Двигаем самолет.
            airplane.MoveUpRight();
        }
    }

    #region объявления класса, унаследованного от точки, объекты которого будут иметь уникальный стиль отображения на карте

    /// <summary>
    /// Самолет, умеющий летать вверх-вправо с заданной скоростью.
    /// </summary>
    [CustomStyle(
        @"new ol.style.Style({
            image: new ol.style.Circle({
                opacity: 1.0,
                scale: 1.0,
                radius: 3,
                fill: new ol.style.Fill({
                    color: 'rgba(255, 0, 255, 0.4)'
                }),
                stroke: new ol.style.Stroke({
                    color: 'rgba(0, 0, 0, 0.4)',
                    width: 1
                }),
            })
        });
        ")] // Переопределим стиль всех объектов данного класса, сделав самолет фиолетовым, используя атрибут CustomStyle.
    class Airplane : Point // Унаследуем данный данный класс от стандартной точки.
    {
        /// <summary>
        /// Скорость самолета.
        /// </summary>
        public double Speed { get; }

        /// <summary>
        /// Конструктор для создания нового объекта.
        /// </summary>
        /// <param name="coordinate">Начальные координаты.</param>
        /// <param name="speed">Скорость.</param>
        public Airplane(Coordinate coordinate, double speed) : base(coordinate) {
            Speed = speed;
        }

        /// <summary>
        /// Двигает самолет вверх-вправо.
        /// </summary>
        public void MoveUpRight() {
            X += Speed;
            Y += Speed;
        }
    }

    #endregion
}